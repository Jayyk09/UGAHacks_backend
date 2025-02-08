import os
from manage_groups import upload_file
from manage_users import update_users_json, create_users_json, update_id_json
from dotenv import load_dotenv
import requests
import json

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
gateway = "jade-petite-jay-124.mypinata.cloud"
key = "I0tNwmegF0rsCpXVDwG56jPb7yO46F4u3mZ_nQbW0hRLf36XDuip2lfEIhup5tto"

def delete_all():
    """Fetch all pinned files and delete each by CID."""
    
    url = "https://api.pinata.cloud/data/pinList"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    # Fetch pinned files
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return

    data = response.json()
    if "rows" not in data:
        print("No files found.")
        return

    files = data["rows"]
    
    if not files:
        print("No pinned files to delete.")
        return

    print(f"Found {len(files)} files. Deleting now...")

    # Iterate through files and delete each by CID
    for file in files:
        cid = file.get("ipfs_pin_hash")
        if cid:
            delete_url = f"https://api.pinata.cloud/pinning/unpin/{cid}"
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 200:
                print(f"Successfully deleted: {cid}")
            else:
                print(f"Failed to delete {cid}. Status code: {delete_response.status_code}")

    print("Deletion process complete.")

def get_all_files():
    url = "https://api.pinata.cloud/v3/files"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        print(response.json())
        return files
    else:
        print(f"Failed to fetch files. Status code: {response.status_code}")
        return None
    
def get_all_users():
    files = get_all_files()
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
    files = get_all_files()
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
    

def create_new_user(name, age, weight, height, sex, address, dob, phone_number):
    result = upload_file(name, age, weight, height, sex, address, dob, phone_number)

    core_id, core_cid = result

    print(core_id, core_cid)

    update_users_json(phone_number, core_id, core_cid)

def setup_db():
    id = create_users_json({})
    update_id_json(id)

def query():
    url = "https://api.pinata.cloud/data/pinList"

    querystring = {"metadata":"age"}

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

# Testing
if __name__ == "__main__":
    # setup_db()
    # create_new_user("beak", 2, 133, 65, "F", "add", "dobb", "111121",)
    # get_all_files()
    # get_files_by_number("2240000")
    # get_all_users()
    # trying()
    # get_by_file("0194e712-969b-717b-8b92-dc2260b5c8fb")
    # print(delete_all())
    query()

