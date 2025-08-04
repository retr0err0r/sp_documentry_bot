from telebot.types import Message, BotCommand

from config import commands_list
from functions.file import process_upload_file, process_show_files
from utils.wrappers import check_username, check_admin


def add_file_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/upload_file", description="📎 Upload File"),
            BotCommand(command="/show_files", description="📎 Show Files for Case")
        ]
    )


def register_upload_file(bot):
    @bot.message_handler(commands=["upload_file"])
    @check_username()
    @check_admin(bot)
    def handle_upload_file(message: Message):
        process_upload_file(message, bot)


def register_show_files(bot):
    @bot.message_handler(commands=["show_files"])
    @check_username()
    @check_admin(bot)
    def handle_show_files(message: Message):
        process_show_files(message, bot)


def file_commands_handler(bot):
    add_file_commands_to_bot()
    register_upload_file(bot)
    register_show_files(bot)
