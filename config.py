import os
from dotenv import load_dotenv

load_dotenv()
AMPLITUDE_API_KEY = os.getenv("AMPLITUDE_API_KEY")
TELEGRAM_CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL")
YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL")
NEW_RELIC_LICENSE_KEY= os.getenv("NEW_RELIC_LICENSE_KEY")

if not AMPLITUDE_API_KEY or not TELEGRAM_CHANNEL_URL or not YOUTUBE_CHANNEL_URL or not NEW_RELIC_LICENSE_KEY:
    raise EnvironmentError("Missing required environment variables: AMPLITUDE_API_KEY or TELEGRAM_CHANNEL_URL or something else")