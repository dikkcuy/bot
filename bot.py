from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext
import requests
import os

# Gantilah dengan token bot Telegram Anda
TELEGRAM_BOT_TOKEN = "7814745652:AAEzioP0y2GJLKOXQNRMjfqUYpcIeHN6gP4"
WEBHOOK_URL = "https://your-domain.com/webhook"

app = Flask(__name__)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# Fungsi untuk mendapatkan informasi IP pengguna
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data["status"] == "success":
            return (f"\U0001F4E1 IP Address: {data['query']}\n"
                    f"\U0001F30E Country: {data['country']}\n"
                    f"\U0001F3E2 ISP: {data['isp']}\n"
                    f"\U0001F4CD Region: {data['regionName']}\n"
                    f"\U0001F4C5 City: {data['city']}\n"
                    f"\U0001F4A1 Timezone: {data['timezone']}")
        else:
            return "IP tidak ditemukan atau terjadi kesalahan."
    except Exception as e:
        return f"Error: {e}"

# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Halo! Kirimkan IP yang ingin Anda cek.")

# Fungsi untuk menangani semua pesan masuk
def detect_user_ip(update: Update, context: CallbackContext) -> None:
    ip = update.message.text
    info = get_ip_info(ip)
    update.message.reply_text(info)

# Menambahkan handler ke dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_user_ip))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
