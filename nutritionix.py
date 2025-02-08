import requests

# Constants
BASE_URL = 'https://trackapi.nutritionix.com/v2/'
HEADERS = {
    'Content-Type': 'application/json',
    'x-app-id': '45285cc0',
    'x-app-key': 'fabe371ce59f86a7cd1dd2efb37b894e',
}

def _post_request(endpoint, query):
    # Makes a POST request and returns the JSON response
    payload = {"query": query}
    response = requests.post(BASE_URL + endpoint, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_macros(info):
    """
    Returns a list of dictionaries containing macro nutrients.
    JSON Format Example:
    [
        {
            "Protein": number,
            "Fat": number,
            "Carbs": number,
            "Calories": number
        },
        ...
    ]
    """
    try:
        data = _post_request('natural/nutrients', info)
        results = []
        for food in data.get('foods', []):
            macros = {}
            for nutrient in food.get('full_nutrients', []):
                attr = nutrient.get('attr_id')
                value = nutrient.get('value')
                if attr == 203:
                    macros['Protein'] = value
                elif attr == 204:
                    macros['Fat'] = value
                elif attr == 205:
                    macros['Carbs'] = value
                elif attr == 208:
                    macros['Calories'] = value
            results.append(macros)
        return results
    except Exception as error:
        return {"error": str(error)}

def get_micros(info):
    """
    Returns a list of dictionaries containing micronutrients.
    JSON Format Example:
    [
        {
            "Vitamin A": number,
            "Vitamin C": number,
            "Vitamin D": number,  # in mcg
            "Vitamin E": number,
            "Vitamin K": number,
            "Thiamin": number,
            "Riboflavin": number,
            "Niacin": number,
            "Vitamin B6": number,
            "Folate": number,
            "Vitamin B12": number,
            "Pantothenic Acid": number,
            "Choline": number,
            "Calcium": number,
            "Chromium": number,
            "Copper": number,
            "Fluoride": number,
            "Iodine": number,
            "Iron": number,
            "Magnesium": number,
            "Manganese": number,
            "Molybdenum": number,
            "Phosphorus": number,
            "Selenium": number,
            "Zinc": number,
            "Potassium": number,
            "Sodium": number,
            "Chloride": number            
        },
        ...
    ]
    """
    try:
        data = _post_request('natural/nutrients', info)
        results = []
        for food in data.get('foods', []):
            micros = {}
            for nutrient in food.get('full_nutrients', []):
                attr = nutrient.get('attr_id')
                value = nutrient.get('value', 0)
                if attr == 320:
                    micros['Vitamin A'] = value
                elif attr == 401:
                    micros['Vitamin C'] = value
                elif attr == 324:
                    micros['Vitamin D'] = value * 40  # convert IU to mcg
                elif attr == 323:
                    micros['Vitamin E'] = value
                elif attr == 430:
                    micros['Vitamin K'] = value
                elif attr == 404:
                    micros['Thiamin'] = value
                elif attr == 405:
                    micros['Riboflavin'] = value
                elif attr == 406:
                    micros['Niacin'] = value
                elif attr == 415:
                    micros['Vitamin B6'] = value
                elif attr == 435:
                    micros['Folate'] = value
                elif attr == 418:
                    micros['Vitamin B12'] = value
                elif attr == 410:
                    micros['Pantothenic Acid'] = value
                elif attr == 421:
                    micros['Choline'] = value
                elif attr == 301:
                    micros['Calcium'] = value
                elif attr == 312:
                    micros['Copper'] = value / 1000 # convert mg to mcg
                elif attr == 313:
                    micros['Fluoride'] = value * 1000 # convert mcg to mg
                elif attr == 303:
                    micros['Iron'] = value
                elif attr == 304:
                    micros['Magnesium'] = value
                elif attr == 315:
                    micros['Manganese'] = value
                elif attr == 305:
                    micros['Phosphorus'] = value
                elif attr == 317:
                    micros['Selenium'] = value
                elif attr == 309:
                    micros['Zinc'] = value
                elif attr == 306:
                    micros['Potassium'] = value
                elif attr == 307:
                    micros['Sodium'] = value
            results.append(micros)
        return results
    except Exception as error:
        return {"error": str(error)}

def get_food_info(info):
    """
    Returns a list of dictionaries containing both macro and micronutrients.
    JSON Format Example:
    [
        {
            "Protein": number,
            "Fat": number,
            "Carbs": number,
            "Calories": number,
            "Vitamin A": number,
            "Vitamin C": number,
            "Vitamin D": number,
            "Vitamin E": number,
            "Vitamin K": number,
            "Thiamin": number,
            "Riboflavin": number,
            "Niacin": number,
            "Vitamin B6": number,
            "Folate": number,
            "Vitamin B12": number,
            "Pantothenic Acid": number,
            "Choline": number,
            "Calcium": number,
            "Chromium": number,
            "Copper": number,
            "Fluoride": number,
            "Iodine": number,
            "Iron": number,
            "Magnesium": number,
            "Manganese": number,
            "Molybdenum": number,
            "Phosphorus": number,
            "Selenium": number,
            "Zinc": number,
            "Potassium": number,
            "Sodium": number,
            "Chloride": number
        },
        ...
    ]
    """
    try:
        data = _post_request('natural/nutrients', info)
        results = []
        mapping = {
            203: 'Protein', 204: 'Fat', 205: 'Carbs', 208: 'Calories', 320: 'Vitamin A',
            401: 'Vitamin C', 324: 'Vitamin D', 323: 'Vitamin E', 430: 'Vitamin K',
            404: 'Thiamin', 405: 'Riboflavin', 406: 'Niacin', 415: 'Vitamin B6',
            435: 'Folate', 418: 'Vitamin B12', 410: 'Pantothenic Acid', 421: 'Choline',
            301: 'Calcium', 312: 'Copper', 313: 'Fluoride', 303: 'Iron', 
            304: 'Magnesium', 310: 'Manganese', 305: 'Phosphorus',
            317: 'Selenium', 309: 'Zinc', 306: 'Potassium', 307: 'Sodium'
        }
        for food in data.get('foods', []):
            info_dict = {}
            for nutrient in food.get('full_nutrients', []):
                attr = nutrient.get('attr_id')
                value = nutrient.get('value', 0)
                if attr in mapping:
                    if attr == 324:
                        info_dict[mapping[attr]] = value * 40
                    elif attr == 312:
                        info_dict[mapping[attr]] = value / 1000 # convert mg to mcg
                    elif attr == 313:
                        info_dict[mapping[attr]] = value * 1000 # convert mcg to mg
                    else:
                        info_dict[mapping[attr]] = value
            results.append(info_dict)
        return results
    except Exception as error:
        return {"error": str(error)}

def get_exercise_info(query="ran 3 miles"):
    """
    Returns a list of dictionaries containing exercise information.
    JSON Format Example:
    [
        {
            "Name": string,
            "Calories Burned": number
        },
        ...
    ]
    """
    try:
        data = _post_request('natural/exercise', query)
        exercises = []
        for exercise in data.get('exercises', []):
            exercises.append({
                "Name": exercise.get("name"),
                "Calories Burned": exercise.get('nf_calories')
            })
        return exercises
    except Exception as error:
        return {"error": str(error)}