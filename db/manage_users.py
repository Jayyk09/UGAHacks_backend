import requests
import os
import json
from dotenv import load_dotenv
from fetch_cid import fetch_cid
import io
from delete_file import delete_file

# Load API keys
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}
JSON_FILE = "cid.json"

# Define the IPNS key name for users.json
IPNS_KEY_NAME = "users.json"

def check_and_delete_json():
    # Check if the file exists
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            if "users.json" in data:
                cid = data["users.json"]
                delete_file(cid)
                print(f"Deleted users.json with CID: {cid}")
                return True
    else:
        print(f"{JSON_FILE} does not exist.")

def update_ipns(key, new_cid):
    """
    Updates the local JSON file with the new CID associated with a given key.
    - `json_file`: The path to the JSON file (e.g., 'cid.json').
    - `key`: The key in the JSON file (e.g., 'users.json').
    - `new_cid`: The new CID to store under the key.
    """    
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}  # If the file doesn't exist, create an empty dictionary
    
    # Update or insert the new CID for the given key
    data[key] = new_cid
    print(f"Updated {key} to {new_cid}")

    # Write the updated data back to the JSON file
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"CID successfully written to {JSON_FILE}")
    except Exception as e:
        print(f"Failed to write CID to {JSON_FILE}: {e}")

def fetch_users_json():
    """Fetches the latest users.json from IPFS."""
    latest_cid = fetch_cid(IPNS_KEY_NAME)
    if not latest_cid:
        print("Not able to fetch users.json. Using empty users.json")
        return {}

    ipfs_url = f"https://gateway.pinata.cloud/ipfs/{latest_cid}"
    response = requests.get(ipfs_url)

    if response.status_code == 200:
        print("Fetched users.json successfully.")
        return response.json()
    else:
        return {}

def post_users_json(raw_json):
    """
    Uploads updated users.json directly to Pinata (IPFS) without creating a file.
    
    - `json_data`: The updated users.json data (Python dictionary)
    
    Returns:
    - New CID of the uploaded file (str) if successful
    - None if the upload fails
    """
    json_bytes = json.dumps(raw_json, indent=4).encode("utf-8")
    json_io = io.BytesIO(json_bytes)

    files = {"file": ("users.json", json_io)}  # Simulate a file upload

    # Define metadata
    metadata = {
        "pinataMetadata": {
            "name": "users.json",
            "keyvalues": {
                "version": "1.0",
                "description": "User group CIDs"
            }
        }
    }

    response = requests.post(PINATA_UPLOAD_URL, headers=HEADERS, files=files, json={"pinataMetadata": json.dumps(metadata)})
    
    if response.status_code == 200:
        new_cid = response.json().get("IpfsHash")
        print(f"File uploaded successfully. New CID: {new_cid}")
        return new_cid
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())
        return None

def update_users_json(action, user_key, value=None):
    """
    Handles updating or deleting entries in users.json without creating a file.
    
    - `action`: "upsert" (modify/add entry) or "delete" (remove entry)
    - `key`: The user or group identifier (e.g., "user_123" or "group_1")
    - `value`: The new CID/IPNS key for the user/group (only for updates)
    """
    raw_json = fetch_users_json()

    if action == "upsert":
        check_and_delete_json()

        raw_json[user_key] = value
        print(f"Updated {user_key} to {value}")
    elif action == "delete":
        check_and_delete_json()

        del raw_json[user_key]
        print(f"Deleted {user_key}")
    else:
        print("Invalid action. Use 'upsert' or 'delete'.")
        return

    new_cid = post_users_json(raw_json)
    if new_cid:
        update_ipns(IPNS_KEY_NAME, new_cid)

def post_user():
    # Define API endpoint and authentication
    url = "https://uploads.pinata.cloud/v3/files"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}"
    }

    # JSON content
    json_data = {
        "user_id": "12345",
        "name": "John Doe",
        "health_records": [
            {"date": "2025-02-08", "diagnosis": "Healthy"}
        ]
    }

    # Convert JSON to a file-like object in memory
    json_bytes = io.BytesIO(json.dumps(json_data).encode("utf-8"))

    # Prepare the request
    files = {
        "file": ("health_data.json", json_bytes, "application/json"),  # Sending as an actual file
    }

    # Send the request
    response = requests.post(url, headers=headers, files=files)

    print(response.json())  # This returns the CID


# Testing
if __name__ == "__main__":
    # action = input("Enter action (upsert/delete): ").strip()
    # user_key = input("Enter user/group key: ").strip()
    # value = None
    # if action == "upsert":
    #     value = input("Enter new CID/IPNS key: ").strip()
    # update_users_json(action, user_key, value)
    post_user()
