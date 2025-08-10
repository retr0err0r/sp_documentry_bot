from telebot.types import Message

from functions.client import process_add_client, process_client_stats, process_list_clients
from utils.wrappers import check_username, check_admin



def register_list_clients(bot):
    @bot.message_handler(commands=['list_clients'])
    @check_username()
    @check_admin(bot)
    def handle_list_clients(message: Message):
        process_list_clients(message, bot)


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
    register_add_client(bot)
    register_list_clients(bot)
    register_client_stats(bot)
