import os
from .manage_groups import upload_file
from .manage_users import update_users_json, create_users_json, update_id_json
from dotenv import load_dotenv
import requests
import json
from typing import List, Tuple, Optional

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

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
    url = "https://api.pinata.cloud/data/pinList"

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}

    querystring = {"pageLimit":"1000", "status":"pinned"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.json())

    return response.json()
    
def get_all_users():
    files = get_all_files()
    if not files:
        return None
    
    res = []
    for file in files.get("rows", []):
        keyvalues = file.get("metadata", {}).get("keyvalues", {})
        for key, val in keyvalues.items():
            if key == "type" and val == "core":
                res.append(file)

    return res

import json

def filter_files_by_queries(queries):
    """
    Filters files based on multiple key-value pairs inside keyvalues.
    Parameters:
        queries (list of tuples): A list of (key, value) pairs to filter by.
            - If value is None, it filters files where key exists.
            - If value is set, it filters files where key exists and matches the value.
    Returns:
        list: A list of filtered files.
    """
    files_data = get_all_files()
    if not files_data:
        return []

    filtered_files = []

    print(files_data)
    for file in files_data.get("rows", []):  # Loop through all files
        print(file)
        keyvalues = file.get("metadata", {}).get("keyvalues", {})

        match = True  # Assume file is a match unless proven otherwise
        for key, value in queries:
            print(key, value, file)
            if key not in keyvalues:
                match = False  # Key is missing, file does not match
                break
            if value is not None and keyvalues[key] != value:
                match = False  # Key exists but value does not match
                break

        if match:
            filtered_files.append(file)

    res = []
    for file in filtered_files:
        cid = file.get("ipfs_pin_hash")
        url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            res.append(json_data)

    print(res)
    return res

    # print(json.dumps(filtered_files, indent=4))  # Pretty print the results

    # for file in filtered_files:

    # return filtered_files

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

    print(res)
    return res
    

def create_new_user(name, age, weight, height, sex, address, phone_number):
    result = upload_file(name, age, weight, height, sex, address, phone_number)

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

def get_all_user_info():
    users = get_all_users()

    print("hi")
    print(users)
    print("hi2")

    res = []
    for user in users:
        cid = user.get("ipfs_pin_hash")
        print(cid)
        url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        response = requests.get(url)
        print(response.text)
        phone_number = user.get("metadata", {}).get("keyvalues", {}).get("id")
        res.append((phone_number, response.json()))

    return res

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
    # query()
    query_1 = [("type", "date"), ("id", "2052391306")]
    # query_2 = [("type", "date")]

    filter_files_by_queries(query_1)
    # get_all_users()