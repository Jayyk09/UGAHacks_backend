import os
from manage_groups import create_and_upload
from manage_users import update_users_json, create_users_json, update_id_json
from dotenv import load_dotenv
import requests

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def fetch_all_files():
    url = "https://api.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        print(files)
        return files
    else:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return None

def get_files_by_number(number):
    files = fetch_all_files()
    if not files:
        return None
    
    res = []
    for file in files.get("rows", []):
        metadata = file.get("data", {})
        keyvalues = metadata.get("keyvalues", {})

        if keyvalues.get("group_id") == number:
            res.append(file)
    
    return res
    

def create_new_user(phone_number, core_data):
    result = create_and_upload(phone_number, core_data)

    core_id, core_cid = result

    print(core_id, core_cid)

    update_users_json(phone_number, core_id, core_cid)

def setup_db():
    id = create_users_json({})
    update_id_json(id)

# Testing
if __name__ == "__main__":
    # setup_db()
    # create_new_user("2247707887", {"keys": "values"})
    fetch_all_files()

