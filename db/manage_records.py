import requests
import os
from dotenv import load_dotenv
import json
import io

load_dotenv()
PINATA_JWT = os.getenv("PINATA_JWT")

def create_record(phone_number, food_info, medication, excercises):
    