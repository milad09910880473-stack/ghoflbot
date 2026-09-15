from pyrogram import Client, filters
import yt_dlp

# اطلاعات ربات (اینجا توکنِ جدیدی که از BotFather گرفتی رو بذار)
API_ID = 12345678  # همون عددِ قبلی
API_HASH = "اینجا_هش_خودت_رو_بنویس"
BOT_TOKEN = "8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58" 

app = Client("GhoflMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("سلام! من ربات قفل موزیک هستم. لینک یوتیوب بفرست تا دانلود کنم.")

@app.on_message(filters.text & filters.regex(r"https?://"))
async def download_song(client, message):
    url = message.text
    await message.reply("دارم دانلود می‌کنم، یکم صبر کن...")
    
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'music.mp3'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    await message.reply_audio("music.mp3")

app.run()

