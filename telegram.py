import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNELS = os.getenv("TELEGRAM_CHANNELS", "").split(",")

def get_telegram_subscribers():
    subscribers = {}
    for channel in CHANNELS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMembersCount?chat_id={channel}"
        response = requests.get(url).json()
        if response.get("ok"):
            subscribers[channel] = response["result"]
        else:
            print(f"Failed to fetch {channel}: {response}")
    return subscribers