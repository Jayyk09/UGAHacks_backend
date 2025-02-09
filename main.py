import json
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Query
from fastapi.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import httpx
from pydantic import BaseModel
from retell import Retell
from custom_types import ConfigResponse, ResponseRequiredRequest
from llm import LLMClient
from nutritionix import get_exercise_info, get_food_info, get_macros, get_micros
from typing import List, Optional, Tuple
from db.endpoints import filter_files_by_queries, get_all_user_info

# Load environment variables
load_dotenv(override=True)
retell = Retell(api_key=os.getenv("RETELL_API_KEY"))

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def format_conversation(post_data):
#     """Formats conversation data received from Retell."""
#     conversation_data = post_data.get("data", {}).get("transcript_object", [])
#     call_id = post_data.get("data", {}).get("call_id", "unknown")
#     timestamp = datetime.utcnow().isoformat()
    
#     formatted_conversation = [{"role": entry["role"], "content": entry["content"]} for entry in conversation_data]
    
#     return {
#         "conversation": formatted_conversation,
#         "call_id": call_id,
#         "timestamp": timestamp,
#     }

# Handle webhook from Retell server. This is used to receive events from Retell server.
# Including call_started, call_ended, call_analyzed
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        post_data = await request.json()
        valid_signature = retell.verify(
            json.dumps(post_data, separators=(",", ":"), ensure_ascii=False),
            api_key=str(os.environ["RETELL_API_KEY"]),
            signature=str(request.headers.get("X-Retell-Signature")),
        )
        if not valid_signature:
            print(
                "Received Unauthorized",
                post_data["event"],
                post_data["data"]["call_id"],
            )
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        if post_data["event"] == "call_started":
            print("Call started event", post_data['call']['from_number'])
        elif post_data["event"] == "call_ended":
            print("Call ended event", post_data)
        elif post_data["event"] == "call_analyzed":
            print("Call analyzed event", post_data['call']['transcript_object'])
            # Extract food items from the analysis
            food_items = post_data['call']['call_analysis']['custom_analysis_data']['meals']
            exercises = post_data['call']['call_analysis']['custom_analysis_data']['exercise']
            medications = post_data['call']['call_analysis']['custom_analysis_data']['medications_taken']
            
            print(f"Food items: {food_items}")
            print(f"Exercises: {exercises}")
            print(f"medications_taken: {medications}")
            
            # TODO: Call Nutritionix API to get nutrition data for each food item
            if food_items != '':
                food_info = get_food_info(food_items)
                print(f"Food info: {food_info}")
            if medications != '':
                print(f"Medications: {medications}")
            if exercises != '':
                exercise_info = get_exercise_info(exercises)
                print(f"Exercises: {exercise_info}")
            
            # Combine food items, exercises, and medications into a single JSON
            # get the date from the post data and format as M_D_YY
            
            # get from number from post data and remove the +1
            to_number = post_data['call']['to_number'].replace('+1', '')
            date = datetime.now().strftime("%m_%d_%y")
            daily_health_data = {
                f"{date}": {
                    "Food Info": food_info if food_items != '' else None,
                    "Medications": medications != '',
                    "Exercises": exercise_info if exercises != '' else None
                }
            }
            print(f"Combined daily health data: {daily_health_data}")
            print(f"From number: {to_number}")
            print(f"Date: {date}")

            

            # Update the user's daily health data
        else:
            print("Unknown event", post_data["event"])
        return JSONResponse(status_code=200, content={"received": True})
    except Exception as err:
        print(f"Error in webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )

@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    """Handles real-time communication with Retell's server over WebSocket."""
    try:
        await websocket.accept()
        llm_client = LLMClient()
        
        # Send initial configuration
        await websocket.send_json(ConfigResponse(
            response_type="config",
            config={"auto_reconnect": True, "call_details": True},
            response_id=1
        ).__dict__)
        
        async def handle_message(request_json):
            try:
                if websocket.client_state != WebSocketState.CONNECTED:
                    print("WebSocket disconnected.")
                    return
                
                interaction_type = request_json.get("interaction_type")
                response_id = request_json.get("response_id", 0)
                
                print(f"Handling interaction type: {interaction_type}")
                
                if interaction_type == "call_details":
                    await websocket.send_json(llm_client.draft_begin_message().__dict__)
                elif interaction_type == "ping_pong":
                    await websocket.send_json({"response_type": "ping_pong", "timestamp": request_json.get("timestamp")})
                elif interaction_type in ("response_required", "reminder_required"):
                    request = ResponseRequiredRequest(
                        interaction_type=interaction_type,
                        response_id=response_id,
                        transcript=request_json.get("transcript", []),
                    )
                    async for event in llm_client.draft_response(request):
                        await websocket.send_json(event.__dict__)
                        if request.response_id < response_id:
                            break
            except Exception as e:
                print(f"Error handling message: {e}")
        
        async for data in websocket.iter_json():
            await handle_message(data)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for call {call_id}")
    except ConnectionTimeoutError:
        print(f"Connection timeout for call {call_id}")
    except Exception as e:
        print(f"WebSocket error for call {call_id}: {e}")
        await websocket.close(1011, "Server error")
    finally:
        print(f"WebSocket connection closed for call {call_id}")

@app.get("/calls/{number}")
async def get_calls(number: str):
    try:
        # Add +1 to the front of the number for making the call
        number = "+1" + number
        
        # Define the Retell API URL and headers
        url = "https://api.retellai.com/v2/list-calls/"
        headers = {
            'Authorization': 'Bearer key_83c76c2b934e13732813046f72d7',
            'Content-Type': 'application/json'
        }
        data = {
            "filter_criteria": {
                "from_number": [number]  # Pass as an array of strings
            }
        }
        
        # Make an asynchronous POST request to the Retell API
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
        
        # Check if the response was successful
        if response.status_code == 200:
            call_responses = response.json()
            if not call_responses:
                return JSONResponse(status_code=404, content={"message": "No calls found"})
            return call_responses
        else:
            return JSONResponse(status_code=response.status_code, content={"message": "Error fetching calls"})
    
    except Exception as e:
        print(f"Error fetching calls for {number}: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
    


BATCH_CALL_URL = "https://api.retellapi.com/v1/batch_calls"

class CallTask(BaseModel):
    to_number: str  # Each task must have a recipient number
    variables: dict = {}  # Optional variables for personalization

class CallRequest(BaseModel):
    from_number: str  # Required
    name: str  # Required (was incorrectly `batch_name`)
    tasks: list[CallTask]  # Required (was incorrectly `contacts`)
    trigger_timestamp: int

def schedule_batch_call(from_number, name, tasks, trigger_timestamp):
    batch_call_response = retell.batch_call.create_batch_call(
        name=name,
        from_number=from_number,
        tasks=tasks,
        trigger_timestamp=trigger_timestamp
    )
    print(batch_call_response.batch_call_id)
    return ("success", batch_call_response)

@app.post("/schedule_call")
def schedule_call(request: CallRequest):
    response = schedule_batch_call(request.from_number, request.name, request.tasks, request.trigger_timestamp)
    return {"status": "success", "data": response}

@app.get("/filter_files")
async def filter_files(
    queries: List[str] = Query(...)
):
    print("Received queries:", queries)
    parsed_queries: List[Tuple[str, Optional[str]]] = []
    for query in queries:
        key, sep, value = query.partition(":")
        parsed_queries.append((key, value))

    print("Parsed queries:", parsed_queries)
    
    filtered_files = filter_files_by_queries(parsed_queries)

    return filtered_files

@app.get("/get_user_info")
async def fetch_user_info():
    try:
        print("Fetching user info")
        users = get_all_user_info()
        return users
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
