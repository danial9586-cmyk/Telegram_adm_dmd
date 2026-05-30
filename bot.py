import os
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

GOFILE_API = "https://api.gofile.io/uploadFile"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام دنیال! فایل یا ویدیو رو بفرست تا برات لینک مستقیم ADM بسازم.")

@bot.message_handler(content_types=['document', 'video'])
def upload_to_gofile(message):
    msg = bot.reply_to(message, "⏳ در حال دریافت فایل از تلگرام...")

    file_id = message.document.file_id if message.document else message.video.file_id
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    # دانلود فایل از تلگرام
    file_data = requests.get(file_url).content
    bot.edit_message_text("⏳ در حال آپلود روی GoFile...", message.chat.id, msg.message_id)

    # آپلود روی GoFile
    files = {'file': (message.document.file_name if message.document else "video.mp4", file_data)}
    response = requests.post(GOFILE_API, files=files).json()

    if response["status"] == "ok":
        direct_link = response["data"]["downloadPage"]
        bot.edit_message_text(f"✅ لینک مستقیم آماده شد:\n{direct_link}", message.chat.id, msg.message_id)
    else:
        bot.edit_message_text("❌ خطا در آپلود. دوباره امتحان کن.", message.chat.id, msg.message_id)

bot.polling()
