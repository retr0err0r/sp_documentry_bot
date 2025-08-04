from telebot.types import Message

from config import ADMIN_KEY
from models import User, get_session


def process_start(bot, message: Message):
    tg_id = str(message.from_user.id)

    session = get_session()
    with session() as db:
        user = db.query(User).filter_by(tg_id=tg_id).first()

        if user:
            if not user.role:
                bot.reply_to(message, "برای تعیین نقش، لطفاً کلید مخصوص خود را وارد کنید:")
                bot.register_next_step_handler(message, ask_for_role, db, user)
            else:
                bot.reply_to(message, f"خوش آمدید {user.name}! نقش شما: {user.role}")
        else:
            # کاربر هنوز توسط ادمین ثبت نشده
            bot.reply_to(message, "شما هنوز توسط مدیر ثبت نشده‌اید. لطفاً با مدیر تماس بگیرید.")


def ask_for_role(message: Message, user, bot):
    session = get_session()
    text = message.text.strip()
    if text == ADMIN_KEY:
        user.role = "admin"
        session.commit()
        bot.reply_to(message, "نقش شما به عنوان ادمین تنظیم شد.")
    else:
        user.role = "client"
        session.commit()
        bot.reply_to(message, "نقش شما به عنوان مشتری تنظیم شد.")
