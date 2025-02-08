import requests
import os
import json
import subprocess
from dotenv import load_dotenv
from fetch_cid import fetch_cid

# Load API keys
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
IPNS_KEY = os.getenv("IPNS_KEY")  # IPNS key for users.json
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}

# Pinata API URL
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}

# Define the IPNS key name for users.json
IPNS_KEY_NAME = "users.json"

def fetch_users_json():
    """Fetches the latest users.json from IPFS."""
    latest_cid = fetch_cid(IPNS_KEY)
    if not latest_cid:
        print("Not able to fetch users.json. Using empty users.json")
        return {"users": {}, "groups": {}}

    ipfs_url = f"https://gateway.pinata.cloud/ipfs/{latest_cid}"
    response = requests.get(ipfs_url)

    if response.status_code == 200:
        print("Fetched users.json successfully.")
        return response.json()
    else:
        return {"users": {}, "groups": {}}

def upload_to_pinata(file_path):
    """Uploads a file to Pinata (IPFS) with metadata and returns the new CID."""
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}

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

def update_ipns(ipns_key_name, new_cid):
    """Updates the IPNS record for users.json to point to the new CID."""
    result = subprocess.run(["ipfs", "name", "publish", "--key=" + ipns_key_name, new_cid], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"IPNS record updated successfully: {result.stdout}")
    else:
        print(f"Failed to update IPNS record: {result.stderr}")

# new_cid = upload_to_pinata(FILE_TO_UPLOAD)
# if new_cid:
#     update_ipns(IPNS_KEY_NAME, new_cid)
data = fetch_users_json()
print(data)
