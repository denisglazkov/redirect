import json
import requests
import logging
from flask import jsonify, request
from config import AMPLITUDE_API_KEY
from user_agents import parse
from tabulate import tabulate
import textwrap
import hashlib
import base64

# Get the existing logger instance
logger = logging.getLogger("flask-app")

def get_device_id():
    """Generates a short, unique device ID based on IP and User-Agent."""
    user_agent = request.headers.get("User-Agent", "unknown")
    ip_address = request.remote_addr or "0.0.0.0"

    unique_string = f"{ip_address}-{user_agent}"
    
    # Generate SHA-256 hash and shorten it
    hash_object = hashlib.sha256(unique_string.encode()).digest()
    device_id = base64.urlsafe_b64encode(hash_object).decode()[:12]  # First 12 chars

    return device_id

def log_request_details(event, source, payload=None):
    """
    Logs common request details for tracking events.
    """
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    cookies = request.headers.get('Cookie')
    parsed_user_agent = parse(user_agent)
    os_info = f"{parsed_user_agent.os.family} {parsed_user_agent.os.version_string}"
    fbclid = request.args.get('fbclid')
    referer = request.headers.get('Referer')
    origin = request.headers.get('Origin')

    # Prepare the data for the table
    table_data = [
        ["Field", "Value"],
        ["OS", wrap_text(os_info or "None")],
        ["Cookies", wrap_text(cookies or "None")],
        ["Event", wrap_text(event or "None")],
        ["Source", wrap_text(source or "None")],
        ["Data", wrap_text(payload or "None")],
        ["IP Address", wrap_text(ip_address or "None")],
        ["User Agent", wrap_text(user_agent or "None")],
        ["Referer", wrap_text(referer or "None")],
        ["Origin", wrap_text(origin or "None")],
        ["FBCLID", wrap_text(fbclid or "None")],
    ]
    # Generate table
    log_table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    # log_data = {
    #     "OS": os_info,
    #     "Cookies": cookies,
    #     "Event": event,
    #     "Source": source,
    #     "Data": payload,
    #     "IP Address": ip_address,
    #     "User Agent": user_agent,
    #     "Referer": referer,
    #     "Origin": origin,
    #     "FBCLID": fbclid,
    # }
    logger.info(f"\n{log_table}")

def send_amplitude_event(user_id, event_name, event_properties):
    """
    Sends an event to Amplitude.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
    }
    ip_address = request.remote_addr or "0.0.0.0"
    data = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [{
            "user_id": user_id,
            "device_id": None if user_id else get_device_id(),
            "event_type": event_name,
            "event_properties": event_properties,
            "ip": ip_address,
        }]
    }
    
    try:
        response = requests.post('https://api2.amplitude.com/2/httpapi', headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            logger.info(f"Amplitude - success: {response.json()}")
        else:
            logger.error(f"Amplitude - error: {response.text}")
            return jsonify({"error": "Failed to track event"}), 500
    except Exception as e:
        logger.error(f"Amplitude - error sending event to Amplitude: {e}")
        return jsonify({"error": "Failed to track event"}), 500
    
    return None

def track_event(params, event_name, additional_properties=None):
    """
    General function to track any event with custom properties.
    """
    source = params.get('source', 'http_api_source')
    user_id = request.args.get('fbclid') or params.get('contact', {}).get('email', None)
    event_properties = {
        "source": source,
        **(additional_properties or {}),
    }
    
    log_request_details(event_name, source, event_properties)
    return send_amplitude_event(user_id, event_name, event_properties)

def track_click(params, event_name):
    """
    Tracks a click event.
    """
    utm_params = {
        'utm_source': params.get('utm_source', "7777"),
        'utm_medium': params.get('utm_medium', "7777"),
        'utm_campaign': params.get('utm_campaign', "7777"),
        'cohort': params.get('cohort'),
        'personalisation': params.get('personalisation'),
        'send_date': params.get('send_date'),
        'utm_content': params.get('utm_content', "7777"),
        'utm_ads': params.get('utm_ads', "7777"),
        'utm_content_name': params.get('utm_content_name', "7777"),
    }
    return track_event(params, event_name, utm_params)

def track_purchase(params, event_name):
    """
    Tracks a purchase event.
    """
    purchase_details = {
        'plan_valid_until': params.get('plan_valid_until'),
        'site_email': params.get('site_email'),
        'plan_order_id': params.get('plan_order_id'),
        'plan_description': params.get('plan_description'),
        'plan_id': params.get('plan_id'),
        'site_name': params.get('site_name'),
        'plan_title': params.get('plan_title'),
        'plan_price': params.get('plan_price'),
        'plan_start_date': params.get('plan_start_date'),
        'contact_id': params.get('contact_id'),
        'plan_cycle_duration': params.get('plan_cycle_duration'),
        'contact': params.get('contact'),
    }
    return track_event(params, event_name, purchase_details)

def track_login(params, event_name):
    """
    Tracks a login event.
    """
    login_details = {
        'contactId': params.get('contactId'),
        'contact': params.get('contact'),
    }
    return track_event(params, event_name, login_details)

def wrap_text(data, width=50):
    """
    Formats text or dictionaries to be displayed in a table.
    Each key-value pair in a dictionary appears on a new row,
    with values wrapped to the specified width.
    """
    if isinstance(data, dict):
        # Convert dictionary to key-value pairs with wrapped values
        wrapped_lines = []
        for key, value in data.items():
            wrapped_value = "\n".join(textwrap.wrap(str(value), width=width))
            wrapped_lines.append(f"{key}: {wrapped_value}")
        return "\n".join(wrapped_lines)
    elif data is None:
        return "None"
    else:
        # Wrap plain text
        return "\n".join(textwrap.wrap(str(data), width=width))