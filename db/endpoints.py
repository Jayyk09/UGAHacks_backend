import os
from manage_groups import create_and_upload
from manage_users import update_users_json, create_users_json, update_id_json
from dotenv import load_dotenv
import requests
import json

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def trying():
    url = "https://gateway.pinata.cloud/ipfs/jade-petite-jay-124.mypinata.cloud/bafkreiby2q3b7afqhk76jvycycnfns7ngyljexcsp4j47mrcbbpirmy5mq"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return None

def get_all_files():
    url = "https://api.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return None
    
def get_all_users():
    files = fetch_all_files()
    if not files:
        return None
    
    res = []
    for file in files.get("data", {}).get("files", []):
        keyvalues = file.get("keyvalues", {})
        for key, val in keyvalues.items():
            try:
                parsed = json.loads(val)
                core_id = parsed.get("core_id")

                if core_id:
                    res.append((key, core_id))

            except json.JSONDecodeError:
                print(f"Failed to parse JSON for file: {file['id']}")
                continue
    print(res)

def get_files_by_number(number):
    files = fetch_all_files()
    if not files:
        return None
    
    res = []
    for file in files.get("data", {}).get("files", []):
        keyvalues = file.get("keyvalues", {})
        if number in keyvalues:
            try:
                parsed = json.loads(keyvalues[number])
                core_id = parsed.get("core_id")

                if core_id:
                    res.append((file, core_id))

            except json.JSONDecodeError:
                print(f"Failed to parse JSON for file: {file['id']}")
                continue

    print(res[0][1])
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
    # create_new_user("224031230", {"keys": "valuesss"})
    # fetch_all_files()
    # get_files_by_number("2240000")
    # get_all_users()
    trying()

