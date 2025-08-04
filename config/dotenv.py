import os
from dotenv import load_dotenv

load_dotenv(os.getenv("TG_BOT_ENV"))

DATABASE_URL=os.getenv("DATABASE_URL")
BOT_TOKEN=os.getenv("BOT_TOKEN")
TOKEN_LOGGING=os.getenv("TOKEN_LOGGING")
LOG_CHANNEL_ID=os.getenv("LOG_CHANNEL_ID")
LOG_DIR=os.getenv("LOG_DIR")
BACKUP_CHANNEL_ID=os.getenv("BACKUP_CHANNEL_ID")
ARCHIVE_CHANNEL_ID=os.getenv("ARCHIVE_CHANNEL_ID")