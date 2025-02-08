import requests
import os
from dotenv import load_dotenv
import json
import io

# Load API key from .env file
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def create_group(group_name):

    url = "https://api.pinata.cloud/v3/files/groups"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }
    payload = {"name": group_name}

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        group_data = response.json()
        print(f"Group '{group_name}' created successfully.")
        return group_data.get("id")
    else:
        print(f"Failed to create group '{group_name}'. Status code: {response.status_code}")
        print(response.json())
        return None

# def upload_file(user_key, file_name, data, group_cid):
#     """Uploads starting files for a user to Pinata and returns its CID."""
#     json_bytes = json.dumps(data, indent=4).encode("utf-8")
#     json_io = io.BytesIO(json_bytes)

#     files = {"file": (file_name, json_io)}

#     metadata = {
#         "pinataMetadata": {
#             "name": file_name,
#             "keyvalues": {
#                 "version": "1.0",
#                 "description": f"User data for {user_key} - {file_name}"
#             }
#         }
#     }

#     response = requests.post(PINATA_UPLOAD_URL, headers=HEADERS, files=files, json={"pinataMetadata": json.dumps(metadata)})

#     if response.status_code == 200:
#         file_id = response.json().get("IpfsHash")
#         print(f"File uploaded successfully. File ID: {file_id}")

#         # put file in group
#         url = f"https://api.pinata.cloud/groups/{group_cid}/cids"
#         headers = {
#             "Authorization": f"Bearer {PINATA_JWT}",
#             "Content-Type": "application/json"
#         }
#         payload = {"cids": [file_id]}

#         put_response = requests.request("PUT", url, json=payload, headers=headers)

#         if put_response.status_code == 200:
#             print(f"File {file_id} added to group {group_cid} successfully.")
#             return file_id
#         else:
#             print(f"Failed to add file {file_id} to group {group_cid}. Status code: {put_response.status_code}")
#             return None
#     else:
#         print(f"Failed to upload file. Status code: {response.status_code}")
#         print(response.json())
#         return None
    
def create_and_upload(user_key, core_data):
    group_id = create_group(user_key)
    
    core_data_id = upload_file(user_key, "core_data.json", core_data, group_cid)
    index_id = upload_file(user_key, "index.json", index_data, group_cid)

    if not core_data_id or not index_id:
        print("Failed to upload all files.")
        return None
    
    return {
        "groupd_cid": group_cid,
        "core_data_cid": core_data_cid,
        "index_cid": index_cid
    }

# Testing
if __name__ == "__main__":
    # # create_and_upload(user_key, core_data)
    # get_cids("0e7354ee-d6fe-4225-8cfe-8f136039df25")

    create_group("test_group")