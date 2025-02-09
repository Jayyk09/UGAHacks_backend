import requests
import os
import json
from dotenv import load_dotenv
from fetch_id import fetch_id
import io

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
JSON_FILE = "cid.json"
USERS_JSON_ID = "users.json"

def update_users_json(number, core_id, core_cid):
    users_id = fetch_id(USERS_JSON_ID)
    url = f"https://api.pinata.cloud/v3/files/{users_id}"
    headers = {"Authorization": f"Bearer {PINATA_JWT}",
               "Content-Type": "application/json"}

    keyvalues = {
        "core_id": core_id,
        "core_cid": core_cid,
    }

    payload = {
        "name": "users.json",
        "keyvalues": {
            number: json.dumps(keyvalues)
        },
    }
    
    response = requests.request("PUT", url, json=payload, headers=headers)
    response.raise_for_status()

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

def get_user(cid):

    url = "https://api.pinata.cloud/data/pinList"

    querystring = {"cid":f"{cid}"}

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.json())

def create_users_json():
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }

    payload = {
        "pinataMetadata": {
            "name": "userProd.json",
        },
        "pinataContent": {
            "a": "be",
        }
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    res = response.json()
    id = res["IpfsHash"]
    print(id)

# Testing
if __name__ == "__main__":

    # create_users_json()
    get_user("QmQ51kaBDvuznb6uM3smRDV8WzbeeibpTEuWFfc8Wa9MsK")
    # update()
    pass
