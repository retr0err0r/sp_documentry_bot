from telebot import TeleBot
from telebot.types import Message

from models import get_session, User, Document, Payment
from utils.checkers import cancel_flow, is_valid_username, is_valid_phone


def process_add_client(message: Message, bot: TeleBot):
    bot.reply_to(message, "نام مشتری را وارد کنید:\n\n(برای لغو فرآیند روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_name, bot)


def get_name(message: Message, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_client = User(name=message.text, role="client")
    bot.reply_to(message, "یوزرنیم تلگرام مشتری را وارد کنید:\n\n(برای لغو فرآیند روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_username, new_client, bot)


def get_username(message: Message, new_client: User, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    username = message.text.strip().lstrip("@")
    if not is_valid_username(message.text):
        bot.reply_to(message, "یوزرنیم نامعتبر است. لطفا یک یوزرنیم معتبر وارد کنید.")
        bot.register_next_step_handler(message, get_username, new_client)
        return
    new_client.username = username
    bot.reply_to(message, "شماره تلفن مشتری را وارد کنید:\n\n(برای لغو فرآیند روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_phone, new_client, bot)


def get_phone(message: Message, new_client: User, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    phone = message.text.strip()
    if not is_valid_phone(phone):
        bot.reply_to(message, "شماره تلفن نامعتبر است. لطفا یک شماره تلفن معتبر وارد کنید.")
        bot.register_next_step_handler(message, get_phone, new_client, bot)
        return
    new_client.phone = phone
    save_user(message, new_client, bot)


def save_user(message: Message, new_client: User, bot: TeleBot):
    session = get_session()
    session.add(new_client)
    session.commit()
    bot.reply_to(message, "مشتری با موفقیت ثبت شد.")


def process_list_clients(message: Message, bot: TeleBot):
    session = get_session()
    clients = session.query(User).filter_by(role="client").all()
    if not clients:
        bot.reply_to(message, "هیچ مشتری ثبت نشده است.")
        return
    client_list = "\n\n".join([f"@{client.username} - {client.name} - Tel: {client.phone}" for client in clients])
    bot.send_message(message.chat.id, f"📋 لیست مشتریان:\n\n{client_list}")


def process_client_stats(message: Message, bot: TeleBot):
    bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
    bot.register_next_step_handler(message, send_client_info, bot)


def send_client_info(message: Message, bot: TeleBot):
    username = message.text.strip().lstrip("@")
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        bot.reply_to(message, "کاربری با این یوزرنیم پیدا نشد.")
        return
    # تعداد پرونده‌ها
    case_count = session.query(Document).filter_by(client_id=user.id).count()
    # فلکسی استفاده شده
    total_flexis = session.query(Document).filter_by(client_id=user.id).with_entities(
        Document.flexis_used_quantity
    ).all()
    flexi_used = sum([f[0] or 0 for f in total_flexis])
    # مانده حساب
    payments = session.query(Payment).filter_by(user_id=user.id).all()
    balance = 0
    for p in payments:
        amount = float(p.amount)
        balance += amount if p.type == "credit" else -amount
    msg = (
        f"📊 آمار مشتری: @{username}\n\n"
        f"📁 تعداد پرونده‌ها: {case_count}\n"
        f"🚛 مجموع فلکسی‌های مصرف‌شده: {flexi_used}\n"
        f"💰 مانده بدهی: {balance} تومان"
    )
    bot.send_message(message.chat.id, msg)
