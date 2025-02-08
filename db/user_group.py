import requests
import os
from dotenv import load_dotenv
import json
import io

# Load API key from .env file
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

# Pinata API URL
PINATA_GROUP_URL = "https://api.pinata.cloud/groups"
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
# HEADERS = {
#     "Authorization": f"Bearer {PINATA_JWT}",
#     "Content-Type": "application/json"
# }
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}


def create_group(group_name):
    """Creates a new group in Pinata."""
    payload = {"name": group_name}

    response = requests.post(PINATA_GROUP_URL, headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        group_data = response.json()
        print(f"Group '{group_name}' created successfully.")
        return group_data.get("id")
    else:
        print(f"Failed to create group '{group_name}'. Status code: {response.status_code}")
        print(response.json())
        return None

def upload_file(user_key, file_name, data, group_cid):
    """Uploads starting files for a user to Pinata and returns its CID."""
    json_bytes = json.dumps(data, indent=4).encode("utf-8")
    json_io = io.BytesIO(json_bytes)

    files = {"file": (file_name, json_io)}

    metadata = {
        "pinataMetadata": {
            "name": file_name,
            "keyvalues": {
                "version": "1.0",
                "description": f"User data for {user_key} - {file_name}"
            }
        }
    }

    response = requests.post(PINATA_UPLOAD_URL, headers=HEADERS, files=files, json={"pinataMetadata": json.dumps(metadata)})

    if response.status_code == 200:
        file_id = response.json().get("IpfsHash")
        print(f"File uploaded successfully. File ID: {file_id}")

        # put file in group
        url = f"https://api.pinata.cloud/groups/{group_cid}/cids"
        headers = {
            "Authorization": f"Bearer {PINATA_JWT}",
            "Content-Type": "application/json"
        }
        payload = {"cids": [file_id]}

        put_response = requests.request("PUT", url, json=payload, headers=headers)

        if put_response.status_code == 200:
            print(f"File {file_id} added to group {group_cid} successfully.")
            return file_id
        else:
            print(f"Failed to add file {file_id} to group {group_cid}. Status code: {put_response.status_code}")
            return None
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())
        return None
    
def create_and_upload(user_key, core_data):
    """Creates a user group and uploads all relevant files like core_data and index."""
    group_cid = create_group(user_key)

    if not group_cid:
        print("Failed to create group.")
        return None
    
    index_data = {}

    core_data_cid = upload_file(user_key, "core_data.json", core_data, group_cid)
    index_cid = upload_file(user_key, "index.json", index_data, group_cid)

    if core_data_cid and index_cid:
        return {
            "groupd_cid": group_cid,
            "core_data_cid": core_data_cid,
            "index_cid": index_cid
        }
    else:
        print("Failed to upload all files.")
        return None
    
def get_cids(user_key):
    """Fetches the CIDs associated with a group."""
    url = f"https://api.pinata.cloud/groups/{user_key}"

    response = requests.request("GET", url, headers=HEADERS)

    if response.status_code == 200:
        print(response.json())


# Testing
if __name__ == "__main__":
    user_key = "user_123"
    core_data = {
        "age": 30,
        "weight": 70,
        "height": 170,
        "health_conditions": ["hypertension"]
    }

    # create_and_upload(user_key, core_data)
    get_cids("0e7354ee-d6fe-4225-8cfe-8f136039df25")
