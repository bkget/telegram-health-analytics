import os, json, logging
from datetime import datetime

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 

async def download_image(client, message, channel_name):
    channel_dir = os.path.join("data/raw/images", channel_name)
    os.makedirs(channel_dir, exist_ok=True)
    file_path = os.path.join(channel_dir, f"{message.id}.jpg")
    await client.download_media(message, file_path)
    return file_path

def log_message(msg):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "scraping.log")
    with open(log_file, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {msg}\n")

def clean_message(msg):
    if msg is None:
        return None

    from_id = None
    if msg.from_id:
        if hasattr(msg.from_id, 'user_id'):
            from_id = str(msg.from_id.user_id)
        elif hasattr(msg.from_id, 'channel_id'):
            from_id = f"channel:{msg.from_id.channel_id}"
        elif hasattr(msg.from_id, 'chat_id'):
            from_id = f"chat:{msg.from_id.chat_id}"

    return {
        "id": msg.id,
        "date": msg.date.isoformat(),
        "text": msg.message,
        "views": msg.views,
        "forwards": msg.forwards,
        "replies": msg.replies.replies if msg.replies else None,
        "post_author": msg.post_author,
        "grouped_id": msg.grouped_id,
        "from_id": from_id,
    }