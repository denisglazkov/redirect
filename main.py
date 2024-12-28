import os
from flask import Flask, request, redirect
from dotenv import load_dotenv
from logging_config import logger
from utils import track_click
from config import AMPLITUDE_API_KEY, TELEGRAM_CHANNEL_URL, YOUTUBE_CHANNEL_URL

app = Flask(__name__)



@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"

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