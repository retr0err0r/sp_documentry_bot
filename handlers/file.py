from telebot.types import Message

from functions.file import process_upload_file, process_show_files
from utils.wrappers import check_username, check_admin


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
    register_upload_file(bot)
    register_show_files(bot)
