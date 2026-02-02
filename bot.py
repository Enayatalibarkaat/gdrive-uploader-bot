import os
from pyrogram import Client, filters
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("gdrive_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def upload_to_drive(file_path, file_name):
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return file.get("id")

@app.on_message(filters.document | filters.video)
def handle_file(client, message):
    msg = message.reply_text("Downloading file...")
    file_path = message.download()

    msg.edit("Uploading to Google Drive...")
    file_id = upload_to_drive(file_path, os.path.basename(file_path))

    drive_link = f"https://drive.google.com/uc?export=download&id={file_id}"
    msg.edit(f"Uploaded!\n\n{drive_link}")

app.run()
