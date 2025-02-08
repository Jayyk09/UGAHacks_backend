import requests
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")
PINATA_DELETE_URL = "https://api.pinata.cloud/pinning/unpin/"
HEADERS = {"Authorization": f"Bearer {PINATA_JWT}"}

def delete_file(cid):
    """Deletes a file from Pinata by its ID (CID)."""
    url = f"{PINATA_DELETE_URL}{cid}"
    
    response = requests.delete(url, headers=HEADERS)

    if response.status_code in [200, 204]:
        print(f"File with ID {cid} deleted successfully.")
        return True
    else:
        print(f"Failed to delete file with ID {cid}. Status code: {response.status_code}")
        return False
    
# Testing
if __name__ == "__main__":
    cid = input("Enter the CID to delete: ").strip()
    delete_file(cid)