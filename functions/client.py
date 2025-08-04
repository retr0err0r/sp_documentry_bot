from telebot import TeleBot
from telebot.types import Message

from models import get_session, User, Document, Payment
from utils.checkers import is_admin

user_register_data = {}


def process_add_client(message: Message, bot: TeleBot):
    if not is_admin(str(message.from_user.id)):
        bot.reply_to(message, "شما ادمین نیستید.")
        return
    bot.reply_to(message, "نام مشتری را وارد کنید:")
    user_register_data[message.chat.id] = {}
    bot.register_next_step_handler(message, get_name)


def process_client_stats(message: Message, bot: TeleBot):
    if not is_admin(str(message.from_user.id)):
        bot.reply_to(message, "فقط ادمین‌ها مجاز به مشاهده آمار هستند.")
        return
    bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
    bot.register_next_step_handler(message, process_username)


def get_name(message: Message, bot: TeleBot):
    user_register_data[message.chat.id]['name'] = message.text
    bot.reply_to(message, "یوزرنیم تلگرام مشتری را وارد کنید:")
    bot.register_next_step_handler(message, get_username)


def get_username(message: Message, bot: TeleBot):
    user_register_data[message.chat.id]['username'] = message.text
    bot.reply_to(message, "شماره تلفن مشتری را وارد کنید:")
    bot.register_next_step_handler(message, save_user)


def save_user(message: Message, bot: TeleBot):
    data = user_register_data.pop(message.chat.id)
    session = get_session()
    with session() as db:
        user = User(
            name=data['name'],
            username=data['username'],
            phone=message.text,
            tg_id="",  # خالی چون مشتری خودش بعدا start میکنه
            role="client"
        )
        db.add(user)
        db.commit()
    bot.reply_to(message, "مشتری با موفقیت ثبت شد.")


def process_username(message: Message, bot: TeleBot):
    username = message.text.strip().lstrip("@")
    session = get_session()
    with session() as db:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            bot.reply_to(message, "کاربری با این یوزرنیم پیدا نشد.")
            return
        # تعداد پرونده‌ها
        case_count = db.query(Document).filter_by(client_id=user.id).count()
        # فلکسی استفاده شده
        total_flexis = db.query(Document).filter_by(client_id=user.id).with_entities(
            Document.flexis_used_quantity
        ).all()
        flexi_used = sum([f[0] or 0 for f in total_flexis])
        # مانده حساب
        payments = db.query(Payment).filter_by(user_id=user.id).all()
        balance = 0
        for p in payments:
            amount = float(p.amount)
            balance += amount if p.type == "credit" else -amount
        msg = (
            f"📊 آمار مشتری: @{username}\n\n"
            f"📁 تعداد پرونده‌ها: {case_count}\n"
            f"🚛 مجموع فلکسی‌های مصرف‌شده: {flexi_used}\n"
            f"💰 مانده حساب: {balance:.2f} تومان"
        )
        bot.send_message(message.chat.id, msg)
