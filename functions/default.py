from telebot import TeleBot
from telebot.types import Message

from models import get_session, User


def process_start(message: Message, bot: TeleBot):
    tg_id = str(message.from_user.id)
    user_role = get_user_role(message.from_user.username)
    if user_role == "admin":
        send_start_msg_to_admin(tg_id, bot)
    elif user_role == "client":
        send_start_msg_to_user(tg_id, bot)
    else:
        text = "با سلام\n⭕️نقش شما در بات ثبت نشده است.\nبرای استفاده از بات مذکور لطفا با بخش پشتیبانی ارتباط حاصل فرمایید.\nبا تشکر."
        bot.send_message(tg_id, text)


def get_user_role(username: str):
    user = get_user(username)
    if user is None:
        return "User not found"
    elif not user.role:
        return "N/A"
    return user.role


def get_user(username: str):
    session = get_session()
    user = session.query(User).filter(User.username == username).first()
    return user


def send_start_msg_to_admin(tg_id: str, bot: TeleBot):
    text = """
با سلام
لطفا از منوی زیر گزینه موردنظر خود را انتخاب کنید:


——- بخش مشتری ——-
/add_client
/list_clients
/client_stats

——- بخش اسناد ——-
/add_case
/cases
/search_case

——- بخش فایل ها و مدارک ——-
/upload_file
/show_files

——- بخش مالی ——-
/add_payment
/balance    
"""
    bot.send_message(tg_id, text)


def send_start_msg_to_user(tg_id: str, bot: TeleBot):
    text = """
با سلام
لطفا از منوی زیر گزینه موردنظر خود را انتخاب کنید:

——- بخش اطلاعات ——-
/client_stats

——- بخش اسناد ——-
/cases
/search_case

——- بخش فایل ها و مدارک ——-
/show_files

——- بخش مالی ——-
/balance
"""
    bot.send_message(tg_id, text)


def process_help(message: Message, bot: TeleBot):
    text = """
گزینه های موجود در منوی اصلی:

/start - شروع کار با ربات
/help - راهنمای استفاده از ربات
/add_client - افزودن مشتری جدید (فقط برای ادمین)
/client_stats - مشاهده آمار مشتریان (فقط برای ادمین)
/add_case - افزودن پرونده جدید (فقط برای ادمین)
/cases - مشاهده پرونده ها 
/search_case - جستجوی پرونده 
/upload_file - بارگذاری فایل جدید (فقط برای ادمین)
/show_files - نمایش فایل ها 
/add_payment - افزودن پرداخت جدید (فقط برای ادمین)
/balance - مشاهده موجودی 
    """
    bot.send_message(message.from_user.id, text)
