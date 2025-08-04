from utils.runner import runner
from telebot import TeleBot

from models.base import init_db
from config import commands_list, BOT_TOKEN
from handlers.admin import admin_commands_handler


# Initialize bot
bot = TeleBot(BOT_TOKEN)

# Initialize Database
init_db()

# Register handlers
admin_commands_handler(bot)

# Set Bot Menu Command
bot.set_my_commands(commands_list)

# Run Bot
runner(bot)