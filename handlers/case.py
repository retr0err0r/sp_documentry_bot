from telebot.types import Message

from functions.case import process_add_case, process_user_case, process_search_case
from utils.wrappers import check_username, check_admin



def register_add_case(bot):
    @bot.message_handler(commands=["add_case"])
    @check_username()
    @check_admin(bot)
    def handle_add_case(message: Message):
        process_add_case(message, bot)


def register_user_case(bot):
    @bot.message_handler(commands=["cases"])
    @check_username()
    def handle_user_case(message: Message):
        process_user_case(message, bot)


def register_search_case(bot):
    @bot.message_handler(commands=["search_case"])
    def handle_search_case(message: Message):
        process_search_case(message, bot)


def case_commands_handler(bot):
    register_add_case(bot)
    register_user_case(bot)
    register_search_case(bot)
