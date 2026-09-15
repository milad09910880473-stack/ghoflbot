import telebot
import yt_dlp

# توکن رباتت
TOKEN = '8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام آق میلاد! ربات تریبون آماده‌ست. لینک موزیک رو بفرست تا برات دانلود کنم.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "دریافت شد! دارم روی موزیک کار می‌کنم...")
    # در اینجا کدهای دانلود با yt-dlp قرار می‌گیره

bot.infinity_polling()
