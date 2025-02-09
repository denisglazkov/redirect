import schedule
import time
from youtube import get_youtube_subscribers
from telegram import get_telegram_subscribers
from amplitude import send_to_amplitude

def collect_and_send_metrics():
    print("📡 Fetching YouTube Subscribers...")
    youtube_data = get_youtube_subscribers()

    print("📡 Fetching Telegram Subscribers...")
    telegram_data = get_telegram_subscribers()

    data = {"youtube": youtube_data, "telegram": telegram_data}
    
    print("📡 Sending to Amplitude...")
    send_to_amplitude("daily_social_metrics", data)

# Schedule to run once per day at midnight
schedule.every().day.at("00:00").do(collect_and_send_metrics)

if __name__ == "__main__":
    print("🚀 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)