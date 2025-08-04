from config import commands_list
from telebot.types import BotCommand, Message
from utils.checkers import is_admin
from models import get_session, Document, User
from functions.case import (
    get_username,
    get_search_key
)
from utils.wrappers import check_username, check_admin
from functions.admin import process_ping


def add_admin_commands_to_bot():
    commands_list.extend(
        [
            BotCommand(command="/ping", description="🔍 Get ping from bot"),
        ]
    )


def register_handlers(bot):
    @bot.message_handler(commands=["add_case"])
    def handle_add_case(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "فقط ادمین‌ها می‌توانند پرونده ثبت کنند.")

        bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
        case_data[message.chat.id] = {}
        bot.register_next_step_handler(message, get_username)


def register_handlers(bot):
    @bot.message_handler(commands=["my_cases"])
    def handle_my_cases(message: Message):
        tg_id = str(message.from_user.id)
        session = get_session()
        with session() as db:
            user = db.query(User).filter_by(tg_id=tg_id).first()
            if not user:
                return bot.reply_to(message, "ابتدا باید توسط مدیر ثبت شوید.")
            docs = db.query(Document).filter_by(client_id=user.id).order_by(Document.id.desc()).limit(5).all()
            if not docs:
                return bot.reply_to(message, "شما هیچ پرونده‌ای ندارید.")
            for doc in docs:
                text = (
                    f"📄 پرونده #{doc.id}\n"
                    f"کوتیج: {doc.cotej_number}\n"
                    f"بوکینگ: {doc.booking_number}\n"
                    f"تعداد کانتینر: {doc.container_quantity}\n"
                    f"وضعیت: {doc.document_status}\n"
                )
                bot.send_message(message.chat.id, text)


def register_handlers(bot):
    @bot.message_handler(commands=["search_case"])
    def handle_search_case(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "فقط ادمین‌ها مجاز به جستجو هستند.")
        bot.reply_to(message, "چه چیزی می‌خواهید جستجو کنید؟ (cotej_number, booking_number, username, document_id)")
        bot.register_next_step_handler(message, get_search_key)


def register_ping(bot):
    @bot.message_handler(commands=["ping"])
    @check_username()
    @check_admin(bot)
    def show_all_users_by_admin(message):
        return process_ping(message, bot)




def admin_commands_handler(bot):
    add_admin_commands_to_bot()
    register_ping(bot)
