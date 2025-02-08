import requests
import os
from dotenv import load_dotenv

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}

def delete_file(id):
    url = f"https://api.pinata.cloud/v3/files/{id}"
    
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 200:
        print(f"File with ID {id} deleted successfully.")
        return True
    else:
        print(f"Failed to delete file with ID {id}. Status code: {response.status_code}")
        return False
    
# Testing
if __name__ == "__main__":
    cid = input("Enter the CID to delete: ").strip()
    delete_file(cid)