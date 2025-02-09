import requests
import os
from dotenv import load_dotenv
import json
import io
from .update import update_file

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

# Define payload data for each date
payloads = {
    "2_8_25": {
        "Food Info": {
            "Protein": 0.2844,
            "Fat": 0.0474,
            "Carbs": 0,
            "Calories": 2.37,
            "Vitamin A": 0,
            "Vitamin C": 0,
            "Vitamin D": 0,
            "Vitamin E": 0.0237,
            "Vitamin K": 0.237,
            "Thiamin": 0.0332,
            "Riboflavin": 0.1801,
            "Niacin": 0.4527,
            "Vitamin B6": 0.0024,
            "Folate": 4.74,
            "Vitamin B12": 0,
            "Pantothenic Acid": 0.602,
            "Choline": 6.162,
            "Calcium": 4.74,
            "Copper": 0.0000047,
            "Fluoride": 214959.0,
            "Iron": 0.0237,
            "Magnesium": 7.11,
            "Manganese": 0,
            "Phosphorus": 7.11,
            "Selenium": 0,
            "Zinc": 0.0474,
            "Potassium": 116.13,
            "Sodium": 4.74
        },
        "Medications": True,
        "Exercises": [
            {
                "Name": "walking",
                "Calories Burned": 61.25
            }
        ]
    },
    "2_9_25": {
        "Food Info": {
            "Protein": 0.312,
            "Fat": 0.052,
            "Carbs": 1.1,
            "Calories": 3.15,
            "Vitamin A": 5,
            "Vitamin C": 2,
            "Vitamin D": 0,
            "Vitamin E": 0.025,
            "Vitamin K": 0.250,
            "Thiamin": 0.035,
            "Riboflavin": 0.190,
            "Niacin": 0.460,
            "Vitamin B6": 0.003,
            "Folate": 5.0,
            "Vitamin B12": 0,
            "Pantothenic Acid": 0.610,
            "Choline": 6.5,
            "Calcium": 5.0,
            "Copper": 0.000005,
            "Fluoride": 215000.0,
            "Iron": 0.025,
            "Magnesium": 7.5,
            "Manganese": 0,
            "Phosphorus": 7.5,
            "Selenium": 0,
            "Zinc": 0.050,
            "Potassium": 118.0,
            "Sodium": 5.0
        },
        "Medications": True,
        "Exercises": [
            {
                "Name": "running",
                "Calories Burned": 120.5
            }
        ]
    },
    "2_10_25": {
        "Food Info": {
            "Protein": 0.290,
            "Fat": 0.048,
            "Carbs": 0.5,
            "Calories": 2.85,
            "Vitamin A": 3,
            "Vitamin C": 1.5,
            "Vitamin D": 0,
            "Vitamin E": 0.024,
            "Vitamin K": 0.240,
            "Thiamin": 0.034,
            "Riboflavin": 0.185,
            "Niacin": 0.455,
            "Vitamin B6": 0.0025,
            "Folate": 4.8,
            "Vitamin B12": 0,
            "Pantothenic Acid": 0.605,
            "Choline": 6.3,
            "Calcium": 4.8,
            "Copper": 0.0000048,
            "Fluoride": 214980.0,
            "Iron": 0.024,
            "Magnesium": 7.2,
            "Manganese": 0,
            "Phosphorus": 7.2,
            "Selenium": 0,
            "Zinc": 0.048,
            "Potassium": 117.5,
            "Sodium": 4.8
        },
        "Medications": True,
        "Exercises": [
            {
                "Name": "cycling",
                "Calories Burned": 90.75
            }
        ]
    },
    "2_11_25": {
        "Food Info": {
            "Protein": 0.275,
            "Fat": 0.045,
            "Carbs": 0.3,
            "Calories": 2.50,
            "Vitamin A": 2,
            "Vitamin C": 1,
            "Vitamin D": 0,
            "Vitamin E": 0.022,
            "Vitamin K": 0.230,
            "Thiamin": 0.032,
            "Riboflavin": 0.175,
            "Niacin": 0.450,
            "Vitamin B6": 0.0022,
            "Folate": 4.6,
            "Vitamin B12": 0,
            "Pantothenic Acid": 0.600,
            "Choline": 6.0,
            "Calcium": 4.6,
            "Copper": 0.0000045,
            "Fluoride": 214950.0,
            "Iron": 0.022,
            "Magnesium": 7.0,
            "Manganese": 0,
            "Phosphorus": 7.0,
            "Selenium": 0,
            "Zinc": 0.045,
            "Potassium": 115.0,
            "Sodium": 4.6
        },
        "Medications": True,
        "Exercises": [
            {
                "Name": "yoga",
                "Calories Burned": 50.25
            }
        ]
    },
    "2_12_25": {
        "Food Info": {
            "Protein": 0.320,
            "Fat": 0.055,
            "Carbs": 1.2,
            "Calories": 3.25,
            "Vitamin A": 6,
            "Vitamin C": 3,
            "Vitamin D": 0,
            "Vitamin E": 0.026,
            "Vitamin K": 0.260,
            "Thiamin": 0.036,
            "Riboflavin": 0.195,
            "Niacin": 0.470,
            "Vitamin B6": 0.0035,
            "Folate": 5.2,
            "Vitamin B12": 0,
            "Pantothenic Acid": 0.620,
            "Choline": 6.7,
            "Calcium": 5.2,
            "Copper": 0.0000052,
            "Fluoride": 215020.0,
            "Iron": 0.026,
            "Magnesium": 7.8,
            "Manganese": 0,
            "Phosphorus": 7.8,
            "Selenium": 0,
            "Zinc": 0.052,
            "Potassium": 120.0,
            "Sodium": 5.2
        },
        "Medications": True,
        "Exercises": [
            {
                "Name": "swimming",
                "Calories Burned": 130.0
            }
        ]
    }
}

number = '2052391306'

# Get list of payload dates
payload_dates = ["2_8_25", "2_9_25", "2_10_25", "2_11_25", "2_12_25"]

def create_payload_and_get_cid(date, phone_number, payload):
    payload = {
        "pinataOptions": {"cidVersion": 1},
        "pinataMetadata": {
            "name": f"{phone_number}_{date}",
            "date": date
        },
        "pinataContent": {
            date: payload
        }
    }

    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json" 
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response_json = response.json()
    return response_json["IpfsHash"]

# Create payloads and get CIDs for each date
cids = []
for date in payload_dates:
    payload = payloads[date]
    cid = create_payload_and_get_cid(date, number, payload)
    cids.append((cid, date))
    print(f"CID for {date}: {cid}")

# Update files with metadata
for cid, date in cids:
    update_file(cid, {"date": date, "type": "date", "id": number})