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

def fetch_existing_metadata(cid):
    url = "https://api.pinata.cloud/data/pinList"

    querystring = {"cid":f"{cid}"}

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    return data['rows'][0]['metadata']['keyvalues'] if data['rows'][0]['metadata']['keyvalues'] else {}

def update_file(cid, new_metadata):
    url = "https://api.pinata.cloud/pinning/hashMetadata"

    existing_metadata = fetch_existing_metadata(cid)
    updated_metadata = {**existing_metadata, **new_metadata}


    payload = {
        "ipfsPinHash": f"{cid}",
        "keyvalues": updated_metadata
    }
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }

    print(payload)

    requests.request("PUT", url, json=payload, headers=headers)

# test
if __name__ == "__main__":
    update_file("QmQ51kaBDvuznb6uM3smRDV8WzbeeibpTEuWFfc8Wa9MsK", {
  "2_8_25": 
    "Food Info" })