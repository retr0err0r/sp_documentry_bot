from telebot.types import Message

from functions.payment import process_add_payment, process_balance


def register_add_payment(bot):
    @bot.message_handler(commands=["add_payment"])
    def handle_add_payment(message: Message):
        process_add_payment(message, bot)


def register_balance(bot):
    @bot.message_handler(commands=["balance"])
    def handle_balance(message: Message):
        process_balance(message, bot)


def payment_commands_handler(bot):
    register_add_payment(bot)
    register_balance(bot)
