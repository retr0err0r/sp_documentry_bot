import logging
import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv(os.getenv("CLOCKIFY_ENV"))


def add_log(the_error):
    log_channel_id = str(os.getenv("LOG_CHANNEL_ID"))
    current_dir = os.path.dirname(os.getenv("CLOCKIFY_LOG_DIR"))
    logging_bot = TeleBot(os.getenv("TOKEN_LOGGING"))
    username = TeleBot(os.getenv("BOT_TOKEN")).get_me().username
    log_filename = os.path.join(current_dir, f"{username}_logs.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.error(the_error)
    logging_bot.send_message(log_channel_id, f"{username} - {the_error}")
