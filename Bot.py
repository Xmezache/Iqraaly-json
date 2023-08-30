import os
import requests
import json
import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot("6413264184:AAGurOdUp19ZmaYgFglVLp4VFrR2nrjacK4")

# Get the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# تحديد الـ IDs التي تريد تنزيل ملفات JSON لها
ids = list(range(1, 2172))

base_url = "https://app.iqraaly.com/api/v3/books/"

headers = {
    "Authorization": "Bearer p1AvJ82pt39GSK42EZiDgwf5bEMZakiniWcvf0AaDAd9QJ3SUiBcsxQqG1ik",
    "User-Agent": "okhttp/3.12.1",
    "app-type": "android",
    "app-version": "4.3.6",
    "device-uniqid": "7c1528fc61b25e8e",
    "local-country": "US"
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل /download لبدء تنزيل الملفات.")

@bot.message_handler(commands=['download'])
def download_files(message):
    for id in ids:
        url = base_url + str(id)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                book_info = response.json()
                file_name = f"{book_info['book']['name']}.json"
                file_path = os.path.join(script_directory, file_name)
                with open(file_path, "w", encoding="utf-8") as json_file:
                    json.dump(book_info, json_file, ensure_ascii=False, indent=2)
                bot.send_message(message.chat.id, f"تم تنزيل الملف: {file_name}")
            else:
                bot.send_message(message.chat.id, f"فشل في تنزيل الملف للـ ID: {id}")
        except Exception as e:
            bot.send_message(message.chat.id, f"حدث خطأ: {e}")

bot.polling()
