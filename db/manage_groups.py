import requests
import os
from dotenv import load_dotenv
import json
import io
from manage_users import update_users_json

# Load API key from .env file
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def create_group(phone_number):
    print(f"Creating group with name: {phone_number}")
    url = "https://api.pinata.cloud/v3/files/groups"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }
    payload = {"name": phone_number}

    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        group_data = response.json()
        print(f"Group '{phone_number}' created successfully.")
        return group_data.get("data", {}).get("id")
    else:
        print(f"Failed to create group '{phone_number}'. Status code: {response.status_code}")
        print(response.json())
        return None

def upload_file(file_name, data, group_id):
    print(f"Uploading file: {file_name} to group: {group_id}")
    keyvalues = {
        key: json.dumps(value) if isinstance(value, dict) else value
        for key, value in data.items()
    }

    metadata = {
        "pinataMetadata": {
            "name": file_name,
            "keyvalues": {
                "group_id": group_id,
            }
        }
    }

    json_bytes = json.dumps(data, indent=4).encode("utf-8")
    json_io = io.BytesIO(json_bytes)
    files = {"file": (file_name, json_io)}

    url = "https://uploads.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    try:
        response = requests.post(url, headers=headers, files=files, json=metadata)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        response_data = response.json()
        file_id = response_data.get("data", {}).get("id")
        file_cid = response_data.get("data", {}).get("cid")
        print(f"File uploaded successfully. File ID: {file_id}, CID: {file_cid}")

        url = f"https://api.pinata.cloud/v3/files/groups/{group_id}/ids/{file_id}"
        headers = {"Authorization": f"Bearer {PINATA_JWT}"}

        try:
            put_response = requests.request("PUT", url, headers=headers)
            put_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

        if put_response.status_code == 200:
            print(f"File {file_id} added to group {group_id} successfully.")
            return file_id, file_cid
        else:
            print(f"Failed to add file {file_id} to group {group_id}. Status code: {put_response.status_code}")
            print(put_response.json())
            return None
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())
        return None
    
def create_and_upload(phone_number, core_data):
    print(f"Creating and uploading for user key: {phone_number}")
    group_id = create_group(phone_number)

    if not group_id:
        print("Failed to create group.")
        return None
    
    core_id, core_cid = upload_file("core.json", core_data, group_id)

    if not core_id:
        print("Failed to upload all files.")
        return None

    return {
        core_id,
        core_cid,
    }

# Testing
if __name__ == "__main__":
    print("Starting test...")
    group_id, core_id, core_cid = create_and_upload("123123123", {"keys": "values"})
    if group_id and core_id and core_cid:
        update_users_json("123123123", core_id, core_cid)
    else:
        print("Test failed.")