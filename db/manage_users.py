import requests
import os
import json
from dotenv import load_dotenv
from fetch_id import fetch_id
import io
from delete_file import delete_file

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
JSON_FILE = "cid.json"
USERS_JSON_ID = "users.json"

def create_users_json(raw_json):
    url = "https://uploads.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    json_bytes = json.dumps(raw_json, indent=4).encode("utf-8")
    json_io = io.BytesIO(json_bytes)
    files = {"file": ("users.json", json_io)}

    metadata = {
        "pinataMetadata": {
            "name": "users.json",
            "keyvalues": {
            }
        }
    }

    response = requests.post(url, headers=headers, files=files, json=metadata)
    response_json = response.json()

    return response_json['data']['id']

def update_id_json(new_id):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    
    data["users.json"] = new_id

    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"ID successfully written to {JSON_FILE}")
    except Exception as e:
        print(f"Failed to write ID to {JSON_FILE}: {e}")

def update_users_json(id):
    url = f"https://api.pinata.cloud/v3/files/{id}"
    headers = {"Authorization": f"Bearer {PINATA_JWT}",
               "Content-Type": "application/json"}
    
    json_data = {
        "name": "John Doe",
        "age": 30,
        "health_data": {
            "blood_type": "O+",
            "allergies": ["Peanuts", "Dust"],
        }
    }

    payload = {
        "name": "users.json",
        "keyvalues": {
            "p": "poop",
            "json_data": json.dumps(json_data)
        }
    }
    
    response = requests.put(url, json=payload, headers=headers)

    print(response.json())

def get_user(latest_id):
    # latest_id = fetch_id(USERS_JSON_ID)

    users_json = f"https://api.pinata.cloud/v3/files/{latest_id}"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    response = requests.get(users_json, headers=headers)

    if response.status_code == 200:
        print("Fetched users.json successfully.")
        print(response.json())
        return response.json()
    else:
        return {}

# Testing
if __name__ == "__main__":
    # action = input("Enter action (upsert/delete): ").strip()
    # user_key = input("Enter user/group key: ").strip()
    # value = None
    # if action == "upsert":
    #     value = input("Enter new CID/IPNS key: ").strip()
    # update_users(action, user_key, value)
    # create_user({"test": "test"})

    # id = create_users_json({})
    # update_id_json(id)
    # update_users_json(id)
    get_user("0194e5b5-8428-7a85-8a6e-8ddcbda002d3")



# def check_and_delete_json():
#     # Check if the file exists
#     if os.path.exists(JSON_FILE):
#         with open(JSON_FILE, "r") as f:
#             data = json.load(f)
#             if "users.json" in data:
#                 id = data["users.json"]
#                 delete_file(id)
#                 print(f"Deleted users.json with CID: {id}")
#                 return True
#     else:
#         print(f"{JSON_FILE} does not exist.")

# def update_users(action, user_key, value=None):
#     raw_json = get_user()

#     if action == "upsert":
#         check_and_delete_json()

#         raw_json[user_key] = value
#         print(f"Updated {user_key} to {value}")
#     elif action == "delete":
#         check_and_delete_json()

#         del raw_json[user_key]
#         print(f"Deleted {user_key}")
#     else:
#         print("Invalid action. Use 'upsert' or 'delete'.")
#         return

#     new_id = create_user(raw_json)
#     if new_id:
#         update_id_json(new_id)