import os
from flask import Flask, request, redirect
from dotenv import load_dotenv
from logging_config import logger
from utils import track_click
from config import AMPLITUDE_API_KEY, TELEGRAM_CHANNEL_URL, YOUTUBE_CHANNEL_URL

app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def hello():
#     return "Hello, World!"

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

if __name__ == '__main__':
    app.run()