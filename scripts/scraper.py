import os
import json
import asyncio
import datetime
import subprocess
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto
from utils import save_json, download_image, log_message, clean_message

# Load environment variables
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
session_name = os.getenv("SESSION_NAME", "anon")
telegram_code = os.getenv("TELEGRAM_CODE")
telegram_password = os.getenv("TELEGRAM_PASSWORD", "")
channels = [
    "https://t.me/HakimedAd",
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/tenamereja"
]

# === Constants ===
DATE_FORMAT = "%Y-%m-%d"
JUNE_START = datetime.datetime(2025, 6, 1, tzinfo=datetime.timezone.utc)
JULY_START = datetime.datetime(2025, 7, 1, tzinfo=datetime.timezone.utc)

# === Directory Setup ===
BASE_DIR = "data/raw"
IMAGE_DIR = os.path.join(BASE_DIR, "images")
MSG_DIR = os.path.join(BASE_DIR, "telegram_messages")

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(MSG_DIR, exist_ok=True)

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        print("Sending login code...")
        await client.send_code_request(phone)

        if not telegram_code:
            raise Exception("TELEGRAM_CODE must be set in .env for first-time login")

        try:
            await client.sign_in(phone=phone, code=telegram_code)
        except SessionPasswordNeededError:
            if telegram_password:
                await client.sign_in(password=telegram_password)
            else:
                raise Exception("2FA password required but TELEGRAM_PASSWORD not provided in .env")

    for channel in channels:
        print(f"📥 Scraping {channel} for June 2025...")

        try:
            entity = await client.get_entity(channel)
            all_messages = []
            offset_id = 0
            image_count = 0
            channel_name = channel.split("/")[-1]

            while True:
                history = await client(GetHistoryRequest(
                    peer=entity,
                    limit=100,
                    offset_date=None,
                    offset_id=offset_id,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                ))

                if not history.messages:
                    break

                for msg in history.messages:
                    msg_date = msg.date.replace(tzinfo=datetime.timezone.utc)
                    if JUNE_START <= msg_date < JULY_START:
                        cleaned = clean_message(msg)

                        if msg.media and isinstance(msg.media, MessageMediaPhoto):
                            if image_count < 10:
                                try:
                                    img_path = await download_image(client, msg, channel_name)
                                    cleaned["image_path"] = img_path
                                    image_count += 1
                                except Exception as e:
                                    log_message(f"⚠️ Failed to download image for msg {msg.id}: {e}")
                            else:
                                log_message(f"ℹ️ Skipped image for msg {msg.id} (100 image limit reached)")

                        all_messages.append(cleaned)

                offset_id = history.messages[-1].id

                if image_count >= 10:
                    log_message(f"✅ Reached 100 image limit for {channel_name}, stopping early.")
                    break

            output_path = os.path.join(MSG_DIR, f"{channel_name}.json")
            save_json(all_messages, output_path)
            print(f"✅ Saved {len(all_messages)} messages to {output_path}")

        except Exception as e:
            error_msg = f"{datetime.datetime.now()} - ❌ Error scraping {channel}: {e}"
            log_message(error_msg)
            print(error_msg)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

    print("🚀 Running dbt transformations...")
    try:
        subprocess.run([
            "dbt", "run",
            "--project-dir", "telegram_dbt",
            "--profiles-dir", os.getenv("DBT_PROFILES_DIR", "/app/.dbt")
        ], check=True)
        print("✅ dbt run completed.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt run failed:", e)