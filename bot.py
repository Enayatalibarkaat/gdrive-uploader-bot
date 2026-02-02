import os
import pickle
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# ===== GOOGLE LOGIN FUNCTION =====
def google_login():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

# ===== /login COMMAND =====
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Login link ban raha hai... browser open hoga")

    service = google_login()

    await update.message.reply_text("✅ Gmail successfully connected!")

# ===== TELEGRAM BOT =====
app = ApplicationBuilder().token("7036939850:AAELrXWVf7f7dYFoZ023mnMIdL8AhxZ33ZU").build()

app.add_handler(CommandHandler("login", login))

print("Bot running...")
app.run_polling()
