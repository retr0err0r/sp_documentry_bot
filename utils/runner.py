import os
import subprocess
import threading
import time
from datetime import datetime as dt
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import schedule
from dotenv import load_dotenv
from telebot import TeleBot

from utils.logger import add_log

load_dotenv(os.getenv("TG_BOT_ENV"))


def backup_command(backup_file, db_name, db_user):
    return [
        "pg_dump", "-h", "localhost", "-p", "5432", "-U", db_user, db_name, "-f", backup_file
    ]


def backup_database(bot):
    db_url = os.getenv("DATABASE_URL")
    url_parts = urlparse(db_url)
    database = {
        'username': url_parts.username,
        'password': url_parts.password,
        'host': url_parts.hostname,
        'port': url_parts.port,
        'name': url_parts.path.lstrip('/')
    }
    os.environ["PGPASSWORD"] = database['password']
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = dt.now(ZoneInfo("Asia/Tehran")).strftime("%Y%m%d_%H%M%S")
    bot_username = bot.get_me().username
    backup_file = os.path.join(backup_dir, f"{bot_username}_{timestamp}.sql")
    command = backup_command(backup_file, database['name'], database['username'])
    try:
        subprocess.run(command, check=True)
        send_backup_to_channel(backup_file)
    except subprocess.CalledProcessError as e:
        add_log(f"Error during backup: {e}")
    else:
        os.remove(backup_file)
    finally:
        if "PGPASSWORD" in os.environ:
            del os.environ["PGPASSWORD"]


def send_backup_to_channel(backup_file):
    logging_bot = TeleBot(os.getenv("TOKEN_LOGGING"))
    log_channel_id = os.getenv("LOG_CHANNEL_ID")
    try:
        with open(backup_file, "rb") as file:
            logging_bot.send_document(os.getenv("BACKUP_CHANNEL_ID"), file)
        logging_bot.send_message(log_channel_id, f"Backup sent successfully: {backup_file}")
    except Exception as e:
        logging_bot.send_message(log_channel_id, f"Error in sending Backup - {e}")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def runner(bot):
    add_log(f"Bot Started at {dt.now(ZoneInfo("Asia/Tehran")).strftime('%Y-%m-%d %H:%M:%S')}")
    threading.Thread(target=run_scheduler, daemon=True).start()
    schedule.every(12).hours.do(job_func=backup_database, bot=bot)
    print("Bot is polling...")
    bot.infinity_polling()
    add_log(f"Bot Stopped at {dt.now(ZoneInfo("Asia/Tehran")).strftime('%Y-%m-%d %H:%M:%S')}")
