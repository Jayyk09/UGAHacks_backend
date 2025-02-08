import requests
import os
from dotenv import load_dotenv
import json
import io

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
# turn this into a json file
# then push the json file to pinata
def create_record(date, phone_number, food_info, medication, exercises):
    combined_json = {
        "food_info": food_info,
        "medication": medication,
        "excercises": exercises
    }

    file_name = f"{date}.json"
    url = "https://uploads.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    metadata = {
        "pinataMetadata": {
            "name": file_name,
            "keyvalues": {
                "group_id": phone_number,
            }
        }
    }
    try:
        json_bytes = json.dumps(combined_json, indent=4).encode("utf-8")
        json_io = io.BytesIO(json_bytes)
        files = {"file": (file_name, json_io)}
        response = requests.post(url, headers=headers, files=files, json=metadata)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


    if response.status_code == 200:
        print(f"File '{file_name}' uploaded successfully.")
        response_data = response.json()
        file_id = response_data.get("data", {}).get("id")
        file_cid = response_data.get("data", {}).get("cid")
        url = f"https://api.pinata.cloud/v3/files/groups/{file_cid}/cids"
        
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