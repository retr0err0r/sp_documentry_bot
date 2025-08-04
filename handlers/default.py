from telebot.types import BotCommand, Message

from config import commands_list
from functions.default import process_start
from utils.wrappers import check_username


def add_default_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/start", description="🤖 start the bot")
        ]
    )


def register_start(bot):
    @bot.message_handler(commands=["start"])
    @check_username()
    def handle_start(message: Message):
        process_start(bot, message)


def default_commands_handler(bot):
    add_default_commands_to_bot()
    register_start(bot)
