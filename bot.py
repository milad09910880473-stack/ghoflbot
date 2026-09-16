import os
from pyrogram import Client, filters
import yt_dlp

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "GhoflMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("سلام آق میلاد! من ربات قفل هستم 🎵\nلینک یوتیوب رو بفرست تا برات دانلود کنم.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def download_song(client, message):
    url = message.text
    if not ("youtube.com" in url or "youtu.be" in url):
        await message.reply("لطفاً یک لینک معتبر یوتیوب بفرستید.")
        return

    status = await message.reply("در حال دانلود موزیک... یکم صبور باش ⏳")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.reply_audio("music.mp3", caption="تقدیم به شما 🎧")
        if os.path.exists("music.mp3"):
            os.remove("music.mp3")
        await status.delete()
    except Exception as e:
        await message.reply(f"خطا در دانلود موزیک: {str(e)}")

app.run()

