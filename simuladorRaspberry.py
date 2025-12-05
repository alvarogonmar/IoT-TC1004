import requests
import time
import random
import json

# Configuration
TARGET_URL = "https://sensor-api-rho.vercel.app/sensor"  # Replace with your actual API endpoint
SLEEP_INTERVAL_SECONDS = 5 * 60  # 5 minutes in seconds
SENSOR_IDS = [1, 2, 3]

 

def send_post_request(url, sensor_id):
    """Sends a POST request to the specified URL with the given payload."""
    try:
        headers = {'Content-Type': 'application/json'}
        value = random.uniform(10, 30)
        full_url = f"{url}/{sensor_id}?value={value}"
        response = requests.post(full_url, headers=headers)
