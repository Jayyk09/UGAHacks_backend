import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

# Pinata API URL
PINATA_GROUP_URL = "https://api.pinata.cloud/v3/files/groups"
HEADERS = {
    "Authorization": f"Bearer {PINATA_JWT}",
    "Content-Type": "application/json"
}

def create_group(group_name):
    """Creates a new group in Pinata."""
    payload = {"name": group_name}

    response = requests.post(PINATA_GROUP_URL, headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        group_data = response.json()
        print(f"Group '{group_name}' created successfully.")
        return group_data.get("id")
    else:
        print(f"Failed to create group '{group_name}'. Status code: {response.status_code}")
        print(response.json())
        return None