import os
from dotenv import load_dotenv

load_dotenv()

# Amplitude API Key
AMPLITUDE_API_KEY = os.getenv("AMPLITUDE_API_KEY")

# YouTube API Key & Channels
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL")
YOUTUBE_CHANNELS = {
    "Yoga Workout System": "UCZFOLrE6NuBgXNtyHRqMlCw",
    "ViC": "UCyayjD6ZIxx4gzPVvJblL5w"
}
# Telegram API Key & Channels
TELEGRAM_CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL")
TELEMETR_API_KEY = os.getenv("TELEMETR_API_KEY")
TELEGRAM_CHANNELS = {
    "Yoga Workout System": "@yws_core"
}


if not AMPLITUDE_API_KEY or not TELEGRAM_CHANNEL_URL or not YOUTUBE_CHANNEL_URL:
    raise EnvironmentError("Missing required environment variables: AMPLITUDE_API_KEY or TELEGRAM_CHANNEL_URL")