import requests
import os
from dotenv import load_dotenv
import json
import io
from manage_users import update_users_json
from update import update_file

# Load API key from .env file
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def upload_file(name, age, weight, height, sex, address, dob, phone_number):
    file_name = "core.json"

    # group_id = create_group(phone_number)

    # if not group_id:
    #     print("Failed to create group.")
    #     return None

    # print(f"Uploading file: {file_name} to group: {group_id}")

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }

    payload = {
        "pinataMetadata": {
            "name": f"{phone_number}.json",
        },
        "pinataContent": {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
        }
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.json()
    id = res["IpfsHash"]
    print(id)

    keyvalues = {
        "name": name,
        "age": str(age),
        "weight": str(weight),
        "height": str(height),
        "sex": sex,
        "address": address,
        "dob": dob,
        "core": "core"
    }

    update_file(id, keyvalues)

    # if response.status_code == 200:
    #     response_data = response.json()
    #     print(response_data)
    #     keyvalues = response_data.get("data", {}).get("keyvalues")
    #     core_id = keyvalues.get("core_id")
    #     core_cid = keyvalues.get("core_cid")

    #     print(f"File uploaded successfully. File ID: {core_id}, CID: {core_cid}")

    #     url = f"https://api.pinata.cloud/v3/files/groups/{group_id}/ids/{core_id}"
    #     headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    #     try:
    #         put_response = requests.request("PUT", url, headers=headers)
    #         put_response.raise_for_status()
    #     except requests.exceptions.RequestException as e:
    #         print(f"Request failed: {e}")
    #         return None

    #     if put_response.status_code == 200:
    #         print(f"File {core_id} added to group {group_id} successfully.")
    #         return core_id, core_cid
    #     else:
    #         print(f"Failed to add file {core_id} to group {group_id}. Status code: {put_response.status_code}")
    #         print(put_response.json())
    #         return None
    # else:
    #     print(f"Failed to upload file. Status code: {response.status_code}")
    #     print(response.json())
    #     return None

# def create_group(phone_number):
#     print(f"Creating group with name: {phone_number}")
#     url = "https://api.pinata.cloud/v3/files/groups"
#     headers = {
#         "Authorization": f"Bearer {PINATA_JWT}",
#         "Content-Type": "application/json"
#     }
#     payload = {"name": phone_number}

#     try:
#         response = requests.request("POST", url, json=payload, headers=headers)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None

#     if response.status_code == 200:
#         group_data = response.json()
#         print(f"Group '{phone_number}' created successfully.")
#         return group_data.get("data", {}).get("id")
#     else:
#         print(f"Failed to create group '{phone_number}'. Status code: {response.status_code}")
#         print(response.json())
#         return None

# Testing
if __name__ == "__main__":
    # print("Starting test...")
    # group_id, core_id, core_cid = create_and_upload("123123123", {"keys": "values"})
    # if group_id and core_id and core_cid:
    #     update_users_json("123123123", core_id, core_cid)
    # else:
    #     print("Test failed.")
    upload_file("Bran Kan", 30, 70, 59, "M", "123 Main St", "1993-01-01", "1234567890")