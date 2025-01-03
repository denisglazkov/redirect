import os
from flask import Flask, request, redirect, render_template_string
from dotenv import load_dotenv
from logging_config import logger
from utils import track_click
from config import AMPLITUDE_API_KEY, TELEGRAM_CHANNEL_URL, YOUTUBE_CHANNEL_URL

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run()