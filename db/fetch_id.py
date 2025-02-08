import json
import os

JSON_FILE = "cid.json"

def fetch_id(key):
    """Fetches the CID for the given key from the local JSON file."""
    try:
        # Check if the JSON file exists
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r") as f:
                data = json.load(f)

            # Check if the key exists in the JSON data
            if key in data:
                latest_cid = data[key]
                print(f"Key '{key}' points to CID: {latest_cid}")
                return latest_cid
            else:
                print(f"Key '{key}' not found in {JSON_FILE}.")
                return None
        else:
            print(f"{JSON_FILE} does not exist.")
            return None
    except Exception as e:
        print(f"Failed to read {JSON_FILE}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    key = input("Enter the key (e.g., 'users.json'): ").strip()
    cid = fetch_id("cid.json", key)
    if cid:
        print(f"🔹 Resolved CID: {cid}")
