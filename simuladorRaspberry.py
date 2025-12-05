import requests
import time
import random
import json

# Configuration
TARGET_URL = "https://sensor-api-rho.vercel.app/sensor"  # Replace with your actual API endpoint
SLEEP_INTERVAL_SECONDS = 5 * 60  # 5 minutes in seconds
SENSOR_IDS = [1, 2, 3]

 

def send_post_request(url, sensor_id):
