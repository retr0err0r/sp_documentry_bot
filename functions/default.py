from models import get_session, User
from telebot.types import Message


def process_start(bot, message: Message):
    tg_id = str(message.from_user.id)
    user_role = get_user_role(tg_id)
    if user_role == "admin":
        send_start_msg_to_admin(bot, tg_id)
    elif user_role == "client":
        send_start_msg_to_user(bot, tg_id)
    else:
        text = "با سلام\n⭕️نقش شما در بات ثبت نشده است.\nبرای استفاده از بات مذکور لطفا با بخش پشتیبانی ارتباط حاصل فرمایید.\nبا تشکر."
        bot.send_message(tg_id, text)


def get_user_role(tg_id: str):
    user = get_user(tg_id)
    if user is None:
        return "User not found"
    elif not user.role:
        return "N/A"
    return user.role


def get_user(tg_id: str):
    session = get_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user


def send_start_msg_to_admin(bot, tg_id: str):
    text = "با سلام\nلطفا از منوی زیر گزینه موردنظر خود را انتخاب کنید:\n\n\n——- بخش مشتری ——-\n/add_client\n/client_stats\n\n——- بخش اسناد ——-\n/add_case\n/cases\n/search_case\n\n——- بخش فایل ها و مدارک ——-\n/upload_file\n/show_files\n\n——- بخش مالی ——-\n/add_payment\n/balance"
    bot.send_message(tg_id, text)


def get_user_name(tg_id: str):
    user = get_user(tg_id)
    if user is None:
        return "کاربر یافت نشد"
    return user.username if user.username else "بدون نام"


def send_start_msg_to_user(bot, tg_id: str):
    text = "با سلام\n\nلطفا از منوی زیر گزینه موردنظر خود را انتخاب کنید:\n\n\n——- بخش مشتری ——-\n/client_stats\n\n——- بخش اسناد ——-\n/cases\n/search_case\n\n——- بخش فایل ها و مدارک ——-\n/show_files\n\n——- بخش مالی ——-\n/balance"
    bot.send_message(tg_id, text)

def process_help(bot, message: Message):
    text = """
گزینه های موجود در منوی اصلی:
/start - شروع کار با ربات
/help - راهنمای استفاده از ربات
/add_client - افزودن مشتری جدید (فقط برای ادمین)
/client_stats - مشاهده آمار مشتریان (فقط برای ادمین)
/add_case - افزودن پرونده جدید (فقط برای ادمین)
/cases - مشاهده پرونده ها (برای همه کاربران)
/search_case - جستجوی پرونده (برای همه کاربران)
/upload_file - بارگذاری فایل جدید (فقط برای ادمین)
/show_files - نمایش فایل ها (برای همه کاربران)
/add_payment - افزودن پرداخت جدید (فقط برای ادمین)
/balance - مشاهده موجودی (برای همه کاربران)
    """
    bot.send_message(message.from_user.id, text)
