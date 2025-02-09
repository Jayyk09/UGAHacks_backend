import requests
import os
from dotenv import load_dotenv
import json
import io
from .update import update_file

# import os
# from manage_groups import create_and_upload
# from manage_users import update_users_json, create_users_json, update_id_json, get_user
# from dotenv import load_dotenv
# import requests
# import json

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

# Define payload data for each date
payload_2_8_25 = {
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
}

payload_2_9_25 = {
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
}

payload_2_10_25 = {
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
}

payload_2_11_25 = {
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
}

payload_2_12_25 = {
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

number = '2052391306'

#different payloads for each day and in different files

# Get list of payload variables
payload_dates = ["2_8_25", "2_9_25", "2_10_25", "2_11_25", "2_12_25"]

# Loop through dates and create separate payloads
# for date in payload_dates:
#     payload = {
#         "pinataOptions": {"cidVersion": 1},
#         "pinataMetadata": {
#             "name": f"{number}_{date}",
#             "date": date
#         },
#         "pinataContent": {
#             date: globals()[f"payload_{date}"]
#         }
#     }

#     headers = {
#         "Authorization": f"Bearer {PINATA_JWT}", 
#         "Content-Type": "application/json"
#     }

#     response = requests.request("POST", url, json=payload, headers=headers)
#     print(f"Response for {date}:")
#     print(response.text)

hashes = [("bafkreibatkmdgeq7qsqm4j7zmtisoe4u7asrgemcczf25oe3kcqpab2d6e", "2_8_25"), ("bafkreihzy7ya3koshdsd3rohamwa3scnrsglvjqq53nyaeuon47rv5amja", "2_9_25"), ("bafkreiaz44hwjwqvpohfjazpxif6bm7kiwclh63etlle4uwnerl6kzh4bu", "2_10_25"), ("bafkreic52ip4h6x7ndhou3vj53pti7crd3o4nurm43k5h5coest6qz7lk4", "2_11_25"), ("bafkreibpjz3irmu2wa56ai37ysow5uxifnt2m7vkqyctiokfwyj3w6w6y4", "2_12_25")]

for hash, date in hashes:
    update_file(hash, {"date": "date", f"{number}_{date}": date })

# load_dotenv()
# PINATA_JWT = os.getenv("PINATA_JWT")
# # turn this into a json file
# # then push the json file to pinata
# def create_record(date, phone_number, food_info, medication, exercises):
#     combined_json = {
#         "food_info": food_info,
#         "medication": medication,
#         "excercises": exercises
#     }

#     file_name = f"{date}.json"
#     url = "https://uploads.pinata.cloud/v3/files"
#     headers = {"Authorization": f"Bearer {PINATA_JWT}"}
#     metadata = {
#         "pinataMetadata": {
#             "name": file_name,
#             "keyvalues": {
#                 "group_id": phone_number,
#             }
#         }
#     }
#     try:
#         json_bytes = json.dumps(combined_json, indent=4).encode("utf-8")
#         json_io = io.BytesIO(json_bytes)
#         files = {"file": (file_name, json_io)}
#         response = requests.post(url, headers=headers, files=files, json=metadata)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None


#     if response.status_code == 200:
#         print(f"File '{file_name}' uploaded successfully.")
#         response_data = response.json()
#         file_id = response_data.get("data", {}).get("id")
#         file_cid = response_data.get("data", {}).get("cid")
#         url = f"https://api.pinata.cloud/v3/files/groups/{file_cid}/cids"
        
#         try:
#             put_response = requests.request("PUT", url, headers=headers)
#             put_response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed: {e}")
#             return None

#         if put_response.status_code == 200:
#             print(f"File {file_id} added to group {group_id} successfully.")
#             return file_id, file_cid
#         else:
#             print(f"Failed to add file {file_id} to group {group_id}. Status code: {put_response.status_code}")
#             print(put_response.json())
#             return None
#     else:
#         print(f"Failed to upload file. Status code: {response.status_code}")
#         print(response.json())
#         return None