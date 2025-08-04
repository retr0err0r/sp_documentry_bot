import logging
import os

from telebot import TeleBot

from config import LOG_CHANNEL_ID, BOT_TOKEN, TOKEN_LOGGING, LOG_DIR


def add_log(the_error):
    log_channel_id = str(LOG_CHANNEL_ID)
    logging_bot = TeleBot(TOKEN_LOGGING)
    username = TeleBot(BOT_TOKEN).get_me().username
    filename = os.path.join(os.path.dirname(LOG_DIR), f"{username}_logs.log")
    logging.basicConfig(
        filename=filename, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.error(the_error)
    logging_bot.send_message(log_channel_id, f"{username} - {the_error}")
