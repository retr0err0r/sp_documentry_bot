from telebot.types import BotCommand, Message

from config import commands_list
from functions.client import process_add_client, process_client_stats
from utils.wrappers import check_username, check_admin


def add_client_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/add_client", description="👔 Add new Client"),
            BotCommand(command="/client_stats", description="👔 Get Client Stats")
        ]
    )


def register_add_client(bot):
    @bot.message_handler(commands=['add_client'])
    @check_username()
    @check_admin(bot)
    def handle_add_client(message: Message):
        process_add_client(message, bot)


def register_client_stats(bot):
    @bot.message_handler(commands=["client_stats"])
    @check_username()
    def handle_client_stats(message: Message):
        process_client_stats(message, bot)


def client_commands_handler(bot):
    add_client_commands_to_bot()
    register_add_client(bot)
    register_client_stats(bot)
