import os
import telebot
from yt_dlp import YoutubeDL

# توکن ربات قفل موزیک
BOT_TOKEN = "8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58"
bot = telebot.TeleBot(BOT_TOKEN)

# ساخت پوشه موقت برای دانلودها
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎧 به ربات **قفل موزیک** خوش آمدید!\n\n"
        "کافیه نام خواننده یا اسم آهنگ مورد نظرت رو برام بفرستی تا برات پیداش کنم و بفرستم."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def search_and_send_music(message):
    query = message.text
    status_msg = bot.reply_to(message, f"🔍 در حال جستجو و دریافت آهنگ «{query}»... لطفاً چند لحظه صبر کنید.")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1:'
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            title = info.get('title', 'music')
            file_path = f"downloads/{title}.mp3"
            
            # ارسال فایل به تلگرام
            with open(file_path, 'rb') as audio:
                bot.send_audio(
                    message.chat.id, 
                    audio, 
                    title=title, 
                    performer="قفل موزیک (GHOFL.M)",
                    caption=f"🎵 {title}\n\n🔒 بات قفل موزیک"
                )
            
            # پاک کردن پیام وضعیت و فایل موقت
            bot.delete_message(message.chat.id, status_msg.message_id)
            if os.path.exists(file_path):
                os.remove(file_path)

    except Exception as e:
        bot.edit_message_text(
            f"❌ متأسفانه در دانلود آهنگ مشکلی پیش آمد یا پیدا نشد.\nارور: {str(e)}", 
            chat_id=message.chat.id, 
            message_id=status_msg.message_id
        )

# روشن نگه داشتن ربات
if __name__ == '__main__':
    print("ربات قفل موزیک روشن شد...")
    bot.infinity_polling()
