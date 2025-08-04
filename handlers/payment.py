from telebot.types import BotCommand, Message

from config import commands_list
from functions.payment import process_add_payment, process_balance


def add_payment_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/add_payment", description="💵 Add new Payment"),
            BotCommand(command="/balance", description="💵 Get Client Balance")
        ]
    )


def register_add_payment(bot):
    @bot.message_handler(commands=["add_payment"])
    def handle_add_payment(message: Message):
        process_add_payment(message, bot)


def register_balance(bot):
    @bot.message_handler(commands=["balance"])
    def handle_balance(message: Message):
        process_balance(message, bot)


def payment_commands_handler(bot):
    add_payment_commands_to_bot()
    register_add_payment(bot)
    register_balance(bot)
