import logging
import pytz
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask import Flask

# Flask setup for Render free tier keepalive
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ CRT Signal Bot is running (keepalive)"

# Your Telegram credentials
TOKEN = "8472184215:AAG7bZCJ6yprFlGFRtN3kB8IflyuRpHLdv8"
CHAT_ID = "6234179043"

# Timezone
IST = pytz.timezone("Asia/Kolkata")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Signal logic (replace with real CRT+SNR detection)
def get_signal():
    now = datetime.now(IST)
    signal = f"📡 CRT Signal [{now.strftime('%H:%M')} IST]\nPAIR: EUR/USD\n🕐 Time: 1 min\n📉 Direction: PUT\n📊 SNR: Strong"
    return signal

# Auto-signal sender
def send_signal(context: CallbackContext):
    try:
        message = get_signal()
        context.bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logger.error("Signal error: %s", e)

# /start command
def start(update, context):
    update.message.reply_text("✅ CRT Signal Bot is active. You'll receive trades here automatically.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Signal every minute
    scheduler = BackgroundScheduler(timezone=IST)
    scheduler.add_job(send_signal, 'cron', second=5, minute='*', args=[updater.bot])
    scheduler.start()

    updater.start_polling()

    # Run Flask to keep alive on Render Web Service
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    main()
