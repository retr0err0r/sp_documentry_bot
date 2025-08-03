import os

from dotenv import load_dotenv
from utils.runner import runner
from telebot import TeleBot

from models import init_db
from config.commands import commands_list

# Load .env file
load_dotenv(os.getenv("TG_BOT_ENV"))

# Initialize bot
bot = TeleBot(os.getenv("BOT_TOKEN"))

# Initialize Database
init_db()

# Register handlers


# Set Bot Menu Command
bot.set_my_commands(commands_list)

# Run Bot
runner(bot)