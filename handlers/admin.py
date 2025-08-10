from functions.admin import (
    process_new_admin,
    process_ping,
)
from utils.wrappers import check_username, check_admin


def register_new_admin_is_here(bot):
    @bot.message_handler(commands=["new_admin_is_here"])
    def new_admin_is_here(message):
        process_new_admin(message, bot)


def register_ping(bot):
    @bot.message_handler(commands=["ping"])
    @check_username()
    @check_admin(bot)
    def show_all_users_by_admin(message):
        process_ping(message, bot)


def admin_commands_handler(bot):
    register_new_admin_is_here(bot)
    register_ping(bot)
