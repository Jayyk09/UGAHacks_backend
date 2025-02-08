from fastapi import FastAPI
from pydantic import BaseModel
from retell import Retell
import requests
import os
from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("RETELL_API_KEY")
# client = Retell(api_key=API_KEY)
# app = FastAPI()
# BATCH_CALL_URL = "https://api.retellapi.com/v1/batch_calls"

# class CallTask(BaseModel):
#     to_number: str  # Each task must have a recipient number
#     variables: dict = {}  # Optional variables for personalization

# class CallRequest(BaseModel):
#     from_number: str  # Required
#     name: str  # Required (was incorrectly `batch_name`)
#     tasks: list[CallTask]  # Required (was incorrectly `contacts`)

# def schedule_batch_call(from_number, name, tasks):
    

#     batch_call_response = client.batch_call.create_batch_call(
#         name=name,
#         from_number=from_number,
#         tasks=tasks
#     )
#     print(batch_call_response.batch_call_id)
        
#     return ("success", batch_call_response)

# @app.post("/schedule_call")
# def schedule_call(request: CallRequest):
#     response = schedule_batch_call(request.from_number, request.name, request.tasks)
#     return {"status": "success", "data": response}
