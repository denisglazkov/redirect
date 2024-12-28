import json

import requests
from flask import jsonify
from logging_config import logger
from config import AMPLITUDE_API_KEY

def track_click(params, event_name):
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
    utm_params = {
        'utm_source': params.get('utm_source', "7777"),
        'utm_medium': params.get('utm_medium', "7777"),
        'utm_campaign': params.get('utm_campaign', "7777"),
        'cohort': params.get('cohort', None),
        'personalisation': params.get('personalisation', None),
        'send_date': params.get('send_date', None)
    }
    event = event_name
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

    return None
