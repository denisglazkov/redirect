import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNELS = os.getenv("YOUTUBE_CHANNELS").split(",")

def get_youtube_subscribers():
    """Fetch YouTube subscriber count for multiple channels."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    subscribers = {}

    for channel_id in YOUTUBE_CHANNELS:
        request = youtube.channels().list(part="statistics", id=channel_id)
        response = request.execute()
        count = response["items"][0]["statistics"]["subscriberCount"]
        subscribers[channel_id] = int(count)

    return subscribers