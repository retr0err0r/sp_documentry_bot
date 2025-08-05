import re

from telebot import TeleBot
from telebot.types import Message

from models.base import get_session
from models.users import User


def is_admin(tg_id: str) -> bool:
    session = get_session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    return user and user.role == "admin"


def cancel_flow(message: Message, bot: TeleBot) -> bool:
    if message.text.lower() == "/cancel":
        bot.reply_to(message, "عملیات لغو شد.")
        return True
    return False


def is_valid_username(username: str) -> bool:
    if not username:
        return False
    if username.startswith("@"):
        username = username[1:]
    return bool(re.match(r"^\w{5,32}$", username, re.ASCII))


def is_valid_phone(phone: str) -> bool:
    """
        Check if the input string is a valid phone number.

        Supports formats:
        - 123-456-7890
        - (123) 456-7890
        - 123 456 7890
        - 123.456.7890
        - +91 1234567890
        - 1234567890
        - with optional country code
    """
    if not phone:
        return False
    pattern = r"^(\+\d{1,3}\s?)?(\(\d{1,4}\)|\d{1,4})[\s\-\.]?\d{1,4}[\s\-\.]?\d{1,4}[\s\-\.]?\d{1,9}$"
    return bool(re.match(pattern, phone))
