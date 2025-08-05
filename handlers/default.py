from telebot.types import Message

from functions.default import process_start, process_help
from utils.wrappers import check_username


def register_start(bot):
    @bot.message_handler(commands=["start"])
    @check_username()
    def handle_start(message: Message):
        process_start(bot, message)


def register_help(bot):
    @bot.message_handler(commands=["help"])
    @check_username()
    def handle_help(message: Message):
        process_help(bot, message)


def default_commands_handler(bot):
    register_start(bot)
    register_help(bot)
