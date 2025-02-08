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

def update_users_json(number, group_id, core_id, core_cid, index_id, index_cid):
    print(number, group_id, core_id, core_cid, index_id, index_cid)
    print(f"Updating users.json for number: {number}")
    users_id = fetch_id(USERS_JSON_ID)
    print(f"Fetched users_id: {users_id}")
    keyvalues = get_user(users_id)
    print(f"Fetched keyvalues: {keyvalues}")
    url = f"https://api.pinata.cloud/v3/files/{users_id}"
    headers = {"Authorization": f"Bearer {PINATA_JWT}",
               "Content-Type": "application/json"}

    keyvalues[str(number)] = json.dumps({
        "group_id": group_id,
        "core_id": core_id,
        "core_cid": core_cid,
        "index_id": index_id,
        "index_cid": index_cid
    })

    payload = {
        "name": "users.json",
        "keyvalues": keyvalues,
    }
    
    try:
        response = requests.request("PUT", url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    print(f"Response from update: {response.json()}")

def get_user(latest_id):
    print(f"Fetching user data for latest_id: {latest_id}")
    users_json = f"https://api.pinata.cloud/v3/files/{latest_id}"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    
    try:
        response = requests.get(users_json, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

    if response.status_code == 200:
        data = response.json()
        keyvalues = data.get("data", {}).get("keyvalues", {})
        print(f"Fetched keyvalues: {keyvalues}")
        return keyvalues
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return {}

def create_users_json(raw_json):
    print("Creating users.json")
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

    try:
        response = requests.post(url, headers=headers, files=files, json=metadata)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    response_json = response.json()
    print(f"Created users.json with ID: {response_json['data']['id']}")
    return response_json['data']['id']

def update_id_json(new_id):
    print(f"Updating ID in {JSON_FILE} with new_id: {new_id}")
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

# Testing
if __name__ == "__main__":
    # print("Starting test...")
    # id = create_users_json({})
    # if id:
    #     update_id_json(id)
    # else:
    #     print("Failed to create users.json")
    # update_users_json(id)
    # get_user("0194e642-b33a-758e-badb-31b19cbbd6b1")
    update_users_json("2247707770", "0194e653-a9e8-71db-ad14-0bad6a0a1875", "0194e646-211c-7027-8728-ab3e3bb6de8c", "bafkreibazhtqmj5tuuvomxjmbfingfyytezx2qrpbhsj6xbvjyydndwa6u", "0194e653-ac2e-75c7-b76c-09f126f52e34", "bafkreicecnx2gvntm6fbcrvnc336qze6st5u7qq7457igegamd3bzkx7ri")
    pass

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