from telebot import TeleBot

from config import commands_list, BOT_TOKEN
from handlers.admin import admin_commands_handler
from handlers.case import case_commands_handler
from handlers.client import client_commands_handler
from handlers.default import default_commands_handler
from handlers.file import file_commands_handler
from handlers.payment import payment_commands_handler
from models.base import init_db
from utils.runner import runner

# Initialize bot
bot = TeleBot(BOT_TOKEN)

# Initialize Database
init_db()

# Register handlers
admin_commands_handler(bot)
payment_commands_handler(bot)
file_commands_handler(bot)
case_commands_handler(bot)
client_commands_handler(bot)
default_commands_handler(bot)

# Set Bot Menu Command
bot.set_my_commands(commands_list)

# Run Bot
runner(bot)
