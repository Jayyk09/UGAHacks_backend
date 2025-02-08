import subprocess

def fetch_cid(ipfs_key):
    """Resolves an IPNS key and returns the latest CID."""
    try:
        result = subprocess.run(["ipfs", "name", "resolve", ipfs_key], capture_output=True, text=True)

        if result.returncode == 0:
            latest_cid = result.stdout.strip().replace("/ipfs/", "")
            print(f"IPNS Key '{ipfs_key}' points to CID: {latest_cid}")
            return latest_cid
        else:
            print(f"Error resolving IPNS ({ipfs_key}):", result.stderr)
            return None
    except Exception as e:
        print("Failed to run IPFS command:", e)
        return None
    
# Testing
if __name__ == "__main__":
    ipns_key = input("Enter IPNS key: ").strip()
    cid = fetch_cid(ipns_key)
    if cid:
        print(f"🔹 Resolved CID: {cid}")