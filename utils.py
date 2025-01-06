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
    payload = {
        'plan_valid_until': params.get('plan_valid_until', None),
        'site_email': params.get('site_email', None),
        'plan_order_id': params.get('plan_order_id', None),
        'plan_description': params.get('plan_description', None),
        'plan_id': params.get('plan_id', None),
        'site_name': params.get('site_name', None),
        'plan_title': params.get('plan_title', None),
        'plan_price': params.get('plan_price', None),
        'plan_start_date': params.get('plan_start_date', None),
        'contact_id': params.get('contact_id', None),
        'plan_cycle_duration': params.get('plan_cycle_duration', None),
        'contact': params.get('contact', None)
    }
    event = event_name
    source = params.get('source', 'http_api_source')
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    parsed_user_agent = parse(user_agent)
    os_info = f"{parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
    logger.info(f"OS: {os_info}")
    logger.info(f"Event: {event}, Source: {source}, Data: {payload}, IP Address: {ip_address}, User Agent: {user_agent}")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }
        data = {
            "api_key": AMPLITUDE_API_KEY,
            "events": [{
                "user_id": params.get('contact').get('email', None),
                "event_type": event,
                "event_properties": {
                    "source": source,
                    **payload,
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

def track_login(params, event_name):
    payload = {
        'contactId': params.get('contactId', None),
        'contact': params.get('contact', None)
    }
    event = event_name
    source = params.get('source', 'http_api_source')
    user_agent = request.headers.get('User-Agent')
    cookies = request.headers.get('Cookie')
    ip_address = request.remote_addr
    parsed_user_agent = parse(user_agent)
    os_info = f"{parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
    logger.info(f"OS: {os_info}")
    logger.info(f"Cookies: {cookies}")
    logger.info(f"Event: {event}, Source: {source}, Data: {payload}, IP Address: {ip_address}, User Agent: {user_agent}")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
        }
        data = {
            "api_key": AMPLITUDE_API_KEY,
            "events": [{
                "user_id": params.get('contact').get('email', None),
                "event_type": event,
                "event_properties": {
                    "source": source,
                    **payload,
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
