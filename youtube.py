import os
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNELS = os.getenv("YOUTUBE_CHANNELS", "").split(",")

def get_youtube_subscribers():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    subscribers = {}
    for channel_id in YOUTUBE_CHANNELS:
        request = youtube.channels().list(part="statistics", id=channel_id)
        response = request.execute()
        count_str = response["items"][0]["statistics"]["subscriberCount"]
        subscribers[channel_id] = int(count_str)
    return subscribers