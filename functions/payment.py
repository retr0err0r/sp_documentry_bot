from telebot import TeleBot
from telebot.types import Message

from models import get_session, User, Payment
from utils.checkers import is_admin

payment_context = {}


def process_add_payment(message: Message, bot: TeleBot):
    if not is_admin(str(message.from_user.id)):
        bot.reply_to(message, "فقط ادمین‌ها مجاز به ثبت پرداخت هستند.")
        return
    bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
    payment_context[message.chat.id] = {}
    bot.register_next_step_handler(message, get_username, bot)


def get_username(message: Message, bot: TeleBot):
    username = message.text.strip().lstrip("@")
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        bot.reply_to(message, "کاربری با این یوزرنیم پیدا نشد.")
        return
    payment_context[message.chat.id]['user_id'] = user.id
    bot.reply_to(message, "مقدار مبلغ (ریال):")
    bot.register_next_step_handler(message, get_amount, bot)


def get_amount(message: Message, bot: TeleBot):
    amount = message.text.strip()
    if not amount.isdigit():
        bot.reply_to(message, "مقدار نامعتبر. لطفاً عدد وارد کنید.")
        return
    payment_context[message.chat.id]['amount'] = amount
    bot.reply_to(message, "نوع: بدهی (`debit`) یا پرداخت (`credit`):", parse_mode="markdown")
    bot.register_next_step_handler(message, get_type, bot)


def get_type(message: Message, bot: TeleBot):
    ptype = message.text.strip().lower()
    if ptype not in ["debit", "credit"]:
        bot.reply_to(message, "نوع باید 'debit' یا 'credit' باشد.")
        return
    payment_context[message.chat.id]['type'] = ptype
    bot.reply_to(message, "توضیح اختیاری:")
    bot.register_next_step_handler(message, save_payment, bot)


def save_payment(message: Message, bot: TeleBot):
    payment_context[message.chat.id]['description'] = message.text
    data = payment_context.pop(message.chat.id)
    session = get_session()
    payment = Payment(**data)
    session.add(payment)
    session.commit()
    bot.reply_to(message, "ثبت پرداخت با موفقیت انجام شد.")


def process_balance(message: Message, bot: TeleBot):
    session = get_session()
    if is_admin(str(message.from_user.id)):
        bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
        bot.register_next_step_handler(message, balance_for_admin, bot)
    else:
        user = session.query(User).filter_by(tg_id=str(message.from_user.id)).first()
        if not user:
            bot.reply_to(message, "شما ثبت نشده‌اید.")
            return
        show_balance(bot, message.chat.id, user.id)


def balance_for_admin(message: Message, bot: TeleBot):
    session = get_session()
    username = message.text.strip().lstrip("@")
    user = session.query(User).filter_by(username=username).first()
    if not user:
        bot.reply_to(message, "کاربر پیدا نشد.")
        return
    show_balance(bot, message.chat.id, user.id)


def show_balance(bot, chat_id, user_id):
    session = get_session()
    payments = session.query(Payment).filter_by(user_id=user_id).all()
    if not payments:
        bot.send_message(chat_id, "تراکنشی ثبت نشده است.")
        return
    total = 0
    lines = []
    for p in payments:
        # """ sign = "+" if p.type == "credit" else "-"  """
        amount = p.amount
        lines.append(f"{p.created_at.date()} | {p.type} | {amount} | {p.description or '-'}")
        total += amount if p.type == "credit" else -amount
    text = "\n".join(lines)
    summary = f"\n\n💰 مانده نهایی: {total} ریال"
    bot.send_message(chat_id, f"📋 لیست تراکنش‌ها:\n{text}{summary}")
