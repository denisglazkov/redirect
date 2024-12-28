import os
from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv
import logging
import requests
import json
from icecream import ic

app = Flask(__name__)
load_dotenv()
AMPLITUDE_API_KEY = os.getenv("AMPLITUDE_API_KEY")
TELEGRAM_CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL")

if not AMPLITUDE_API_KEY or not TELEGRAM_CHANNEL_URL:
    raise EnvironmentError("Missing required environment variables: AMPLITUDE_API_KEY or TELEGRAM_CHANNEL_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"

@app.route('/telegram', methods=['GET'])
def track_click():
    """
    Handles the /telegram route to track a click event and redirect to a Telegram channel URL.

    This function performs the following steps:
    1. Logs the start of the function using the icecream library.
    2. Extracts UTM and other parameters the request.
    3. Logs the event details.
    4. Sends the event data to the Amplitude API.
    5. Handles the response from the Amplitude API.
    6. Redirects the user to the Telegram channel URL.

    Returns:
        A redirect response to the Telegram channel URL or a JSON error response.
    """
    params = request.args
    utm_params = {
        'utm_source': params.get('utm_source', None),
        'utm_medium': params.get('utm_medium', None),
        'utm_campaign': params.get('utm_campaign', None),
        'cohort': params.get('cohort', None),
        'send_date': params.get('send_date', None)
    }
    event = params.get('event', 'telegram')
    source = params.get('source', 'http_api_source')
    logger.info(f"Event: {event}, Source: {source}, UTM Params: {utm_params}")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }
        data = {
            "api_key": AMPLITUDE_API_KEY,
            "events": [{
                "device_id": "<INSERT DEVICE ID>",
                "event_type": event,
                "event_properties": {
                    "source": source,
                    **utm_params,
                }
            }]
        }
        response = requests.post('https://api2.amplitude.com/2/httpapi',
                                 headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logger.info(f"Success: {response.json()}")
        else:
            logger.error(f"Error: {response.text}")
            return jsonify({"error": "Failed to track event"}), 500
    except Exception as e:
        logger.error(f"Error sending event to Amplitude: {e}")
        return jsonify({"error": "Failed to track event"}), 500

    return redirect(TELEGRAM_CHANNEL_URL, code=302)

#for local test
if __name__ == '__main__':
    """
    Entry point for running the Flask application locally.

    This block of code performs the following steps:
    1. Logs a warning indicating that the server is for development only.
    2. Runs the Flask application on the specified host and port.

    Note:
        For production, it is recommended to use Gunicorn.
    """
    port = 8080
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)