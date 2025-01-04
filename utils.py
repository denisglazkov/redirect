import json
import requests
from flask import jsonify, request
from logging_config import logger
from config import AMPLITUDE_API_KEY
from user_agents import parse


def track_click(params, event_name):
    utm_params = {
        'utm_source': params.get('utm_source', "7777"),
        'utm_medium': params.get('utm_medium', "7777"),
        'utm_campaign': params.get('utm_campaign', "7777"),
        'cohort': params.get('cohort', None),
        'personalisation': params.get('personalisation', None),
        'send_date': params.get('send_date', None),
        'utm_content': params.get('utm_content', "7777"),
        'utm_ads': params.get('utm_ads', "7777"),
        'utm_content_name': params.get('utm_content_name', "7777")
    }
    event = event_name
    source = params.get('source', 'http_api_source')
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    parsed_user_agent = parse(user_agent)
    os_info = f"{parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
    logger.info(f"OS: {os_info}")
    logger.info(f"Event: {event}, Source: {source}, UTM Params: {utm_params}, IP Address: {ip_address}, User Agent: {user_agent}")
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

def track_purchase(params, event_name):
    data = {
        'plan_valid_until': params.get('plan_valid_until', '-'),
        'site_email': params.get('site_email', '-'),
        'plan_order_id': params.get('plan_order_id', '-'),
        'plan_description': params.get('plan_description', '-'),
        'plan_id': params.get('plan_id', '-'),
        'site_name': params.get('site_name', '-'),
        'plan_title': params.get('plan_title', '-'),
        'plan_price.value': params.get('plan_price', {}),
        'plan_start_date': params.get('plan_start_date', '-'),
        'contact_id': params.get('contact_id', '-'),
        'plan_cycle_duration': params.get('plan_cycle_duration', '-'),
        'contact': params.get('contact', {})
    }
    event = event_name
    source = params.get('source', 'http_api_source')
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    parsed_user_agent = parse(user_agent)
    os_info = f"{parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
    logger.info(f"OS: {os_info}")
    logger.info(f"Event: {event}, Source: {source}, Data: {data}, IP Address: {ip_address}, User Agent: {user_agent}")
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
                    **data,
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
