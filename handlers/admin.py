from telebot.types import BotCommand

from config.commands import commands_list
from functions.admin import (
    process_new_admin,
    process_ping,
)
from utils.wrappers import check_username, check_admin


def add_admin_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/ping", description="🔍 Get ping from bot"),
        ]
    )


def register_new_admin_is_here(bot):
    @bot.message_handler(commands=["new_admin_is_here"])
    def new_admin_is_here(message):
        return process_new_admin(message, bot)


def register_ping(bot):
    @bot.message_handler(commands=["ping"])
    @check_username()
    @check_admin(bot)
    def show_all_users_by_admin(message):
        return process_ping(message, bot)


def admin_commands_handler(bot):
    add_admin_commands_to_bot()
    register_new_admin_is_here(bot)
    register_ping(bot)
