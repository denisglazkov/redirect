import os
import json
from flask import Flask, request, redirect, render_template_string, jsonify
from dotenv import load_dotenv
from utils import track_click, track_purchase, track_login
from config import AMPLITUDE_API_KEY, TELEGRAM_CHANNEL_URL, YOUTUBE_CHANNEL_URL
import logging
import newrelic.agent
from youtube import get_youtube_subscribers
from telegram import get_telegram_subscribers
from amplitude import send_to_amplitude
import datetime
from notion_utils import insert_notion_row, get_last_two_entries_for_source, extract_count_from_page

# Determine the environment (default to development)
environment = os.getenv("FLASK_ENV", "development")

# Initialize New Relic with the correct environment
newrelic.agent.initialize('newrelic.ini',environment)

# Flask app setup
app = Flask(__name__)

# Set up the logger
logger = logging.getLogger("flask-app")
logger.setLevel(logging.INFO)

# Console handler for local debugging
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)


@app.route('/', methods=['GET'])
def hello():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>Welcome to our tracking server.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/telegram', methods=['GET'])
def track_click_telegram():
    params = request.args
    track_click(params=params, event_name="telegram")
    return redirect(TELEGRAM_CHANNEL_URL, code=302)

@app.route('/youtube', methods=['GET'])
def track_click_youtube():
    params = request.args
    track_click(params=params, event_name="youtube")
    return redirect(YOUTUBE_CHANNEL_URL, code=302)

@app.route('/purchase', methods=['POST'])
def track_purchase_wix():
    params = request.json.get("data")
    logger.info(f"PAYLOAD: {params}")
    track_purchase(params=params, event_name="purchase")
    return {"message": "Purchase tracked successfully!"}, 200

@app.route('/login', methods=['POST'])
def track_login_wix():
    params = request.json.get("data")
    logger.info(f"PAYLOAD: {params}")
    track_login(params=params, event_name="login")
    return {"message": "Login tracked successfully!"}, 200

@app.route("/collect-metrics", methods=["GET"])
def collect_metrics():
    youtube_data = get_youtube_subscribers()
    telegram_data = get_telegram_subscribers()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    
    for channel, subs in youtube_data.items():
        insert_notion_row(source=channel, count=subs, when=now_utc)
        # Optional: send raw count to Amplitude
        send_to_amplitude({
            "event_type": "youtube_subscribers",
            "user_id": "system",
            "event_properties": {
                "channel": channel,
                "subscribers": subs
            },
            "time": int(now_utc.timestamp() * 1000)
        })
        
    for channel, subs in telegram_data.items():
        insert_notion_row(source=channel, count=subs, when=now_utc)
        send_to_amplitude({
            "event_type": "telegram_subscribers",
            "user_id": "system",
            "event_properties": {
                "channel": channel,
                "subscribers": subs
            },
            "time": int(now_utc.timestamp() * 1000)
        })


    return jsonify({
        "status": "success",
        "message": "Collected metrics and stored them in Notion.",
        "data": {
            "youtube": youtube_data,
            "telegram": telegram_data
        }
    })

@app.route("/collect-deltas", methods=["GET"])
def collect_deltas():
    """
    1) For each channel (YouTube + Telegram),
        - Get last 2 Notion entries 
        - Compute delta
        - If delta > 0, send 'new_subscribers' event to Amplitude
    2) Return a JSON summary
    """
    # Combine your known channels
    # (Alternatively, read them from environment again if you prefer)
    from youtube import YOUTUBE_CHANNELS
    from telegram import CHANNELS as TELEGRAM_CHANNELS
    all_sources = YOUTUBE_CHANNELS + TELEGRAM_CHANNELS
    
    results = {}

    for channel in all_sources:
        pages = get_last_two_entries_for_source(channel)
        if len(pages) < 2:
            results[channel] = "Not enough data in Notion (need 2 rows)."
            continue
        
        recent_count = extract_count_from_page(pages[0])
        prev_count   = extract_count_from_page(pages[1])
        delta = recent_count - prev_count

        send_to_amplitude({
            "event_type": "new_subscribers",
            "user_id": "delta_calculator",
            "event_properties": {
                "channel": channel,
                "delta": delta
            },
            "time": int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
        })
        results[channel] = f"Delta = {delta} (event sent)"


    return jsonify({
        "status": "success",
        "results": results
    })



if __name__ == '__main__':
    app.run()