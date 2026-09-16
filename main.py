import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

# --- اطلاعات رباتت ---
API_ID = 12345678  # عدد api_id از my.telegram.org (اگه نداری موقتاً بذار همینو، بعد عوض کن)
API_HASH = "اینجا_هش_تلگرامت_رو_بنویس"
BOT_TOKEN = "8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58"

# آیدی کانالت که میخوای آهنگ‌ها خودکار بره اونجا (ربات باید ادمین کانالت باشه)
CHANNEL_ID = "@MyChannelID"  # به جای این، آیدی کانال خودت رو بذار

app = Client("GhoflMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# پیام استارت
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    text = (
        "🎧 به ربات **GHOFL.M | قـ؋ـل‌موزیک** خوش اومدی!\n\n"
        "کافیه اسم هر آهنگی که می‌خوای رو بفرستی تا برات پیداش کنم و بفرستم. 🎵"
    )
    await message.reply_text(text)

# وقتی کاربر اسم آهنگ میده
@app.on_message(filters.text & ~filters.command(["start"]))
async def download_music(client: Client, message: Message):
    query = message.text.strip()
    status_msg = await message.reply_text("🔎 در حال جستجو و قفل کردن روی موزیک...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }

    try:
        # جستجو در یوتیوب
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if not info or 'entries' not in info or len(info['entries']) == 0:
                await status_msg.edit_text("❌ متأسفانه آهنگی با این اسم پیدا نشد!")
                return
            
            entry = info['entries'][0]
            title = entry.get('title', 'Music')
            duration = entry.get('duration', 0)
            file_name = ydl.prepare_filename(entry)
            audio_file = os.path.splitext(file_name)[0] + ".mp3"

        await status_msg.edit_text("⚡️ آهنگ آماده شد! در حال آپلود...")

        # ارسال برای کاربر
        caption = f"🎵 **{title}**\n\n🆔 @GhoflMusicBot"
        sent_audio = await message.reply_audio(
            audio=audio_file,
            caption=caption,
            duration=duration,
            title=title
        )

        # ارسال خودکار به کانال (اگه کانال ست شده باشه)
        if CHANNEL_ID and CHANNEL_ID != "@MyChannelID":
            try:
                await client.send_audio(
                    chat_id=CHANNEL_ID,
                    audio=audio_file,
                    caption=f"🎵 آهنگ ارسالی جدید در کانال:\n**{title}**\n\n🤖 @GhoflMusicBot",
                    duration=duration,
                    title=title
                )
            except Exception as e:
                print(f"ارور در ارسال به کانال: {e}")

        await status_msg.delete()

        # پاک کردن فایل دانلود شده برای پر نشدن رم/دیسک
        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        await status_msg.edit_text(f"⚠️ خطایی رخ داد: {e}")

print("ربات GHOFL.M آنلاین شد...")
app.run()
