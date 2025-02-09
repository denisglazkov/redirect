import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

AMPLITUDE_API_KEY = os.getenv("AMPLITUDE_API_KEY")

def send_to_amplitude(data):
    """Send events to Amplitude."""
    url = "https://api2.amplitude.com/2/httpapi"
    headers = {"Content-Type": "application/json"}
    
    event = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [
            data
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(event))
    
    if response.status_code == 200:
        print("✅ Data sent to Amplitude:", data)
    else:
        print("❌ Failed to send data:", response.text)