import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")
if not API_KEY:
    raise ValueError("OPENAQ_API_KEY not found in .env file")

BASE_URL = "https://api.openaq.org/v3"

LATITUDE = 27.7172
LONGITUDE = 85.3240
RADIUS = 25000

PARAMETERS = ["pm25", "pm10", "o3"]

DATE_FROM = "2024-01-01T00:00:00Z"
DATE_TO = "2026-02-24T23:59:59Z"

LIMIT = 1000