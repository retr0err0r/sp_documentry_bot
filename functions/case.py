import jdatetime
from telebot import TeleBot
from telebot.types import Message

from models import get_session, User, Document
from utils.buttons import create_reply_buttons
from utils.checkers import is_admin, cancel_flow


def process_add_case(message: Message, bot: TeleBot):
    bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:\n\n(برای لغو روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_username)


def get_username(message: Message, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    session = get_session()
    username = message.text.strip().lstrip("@")
    user = session.query(User).filter_by(username=username).first()
    if not user:
        bot.reply_to(message, "مشتری یافت نشد.")
        return
    new_doc = Document(client_id=user.id)
    bot.reply_to(message, "شماره بوکینگ را وارد کنید:\n\n(برای لغو روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_booking, new_doc, bot)


def get_booking(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.booking_number = message.text
    markup = create_reply_buttons(['5', '10'])
    bot.reply_to(message, "تعداد کانتینر:\n\n(برای لغو روی /cancel کلیک کنید)", reply_markup=markup)
    bot.register_next_step_handler(message, get_container_quantity, new_doc, bot)


def get_container_quantity(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.container_quantity = int(message.text)
    markup = create_reply_buttons(['20', '40'])
    bot.reply_to(message, "سایز کانتینر (فوت):\n\n(برای لغو روی /cancel کلیک کنید)", reply_markup=markup)
    bot.register_next_step_handler(message, get_container_size, new_doc, bot)


def get_container_size(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.container_size = message.text
    markup = create_reply_buttons(["فلکسی"])
    bot.reply_to(message, "نوع کالا:\n\n(برای لغو روی /cancel کلیک کنید)", reply_markup=markup)
    bot.register_next_step_handler(message, get_goods_type, new_doc, bot)


def get_goods_type(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.goods_type = message.text
    today = jdatetime.date.today()
    markup = create_reply_buttons([today.strftime("%Y-%m-%d")])
    bot.reply_to(message, "تاریخ واگذاری (YYYY-MM-DD):\n\n(برای لغو روی /cancel کلیک کنید)", reply_markup=markup)
    bot.register_next_step_handler(message, get_assignment_date, new_doc, bot)


def get_assignment_date(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.assignment_date = message.text
    bot.reply_to(message, "شرکت کشتیرانی:\n\n(برای لغو روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_shipping_company, new_doc, bot)


def get_shipping_company(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.shipping_company = message.text
    bot.reply_to(message, "صاحب کالا:\n\n(برای لغو روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_cargo_owner, new_doc, bot)


def get_cargo_owner(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.cargo_owner = message.text
    bot.reply_to(message, "واحد تولیدی:\n\n(برای لغو روی /cancel کلیک کنید)")
    bot.register_next_step_handler(message, get_production_center, new_doc, bot)


def get_production_center(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.production_center = message.text
    markup = create_reply_buttons(["اعلام بوکینگ", "اتمام سند"])
    bot.reply_to(message, "وضعیت سند:\n\n(برای لغو روی /cancel کلیک کنید)", reply_markup=markup)  # add first status button
    bot.register_next_step_handler(message, get_document_status, new_doc, bot)


def get_document_status(message: Message, new_doc: Document, bot: TeleBot):
    if cancel_flow(message, bot):
        return
    new_doc.document_status = message.text
    save_document_in_db(new_doc)
    bot.reply_to(message, "پرونده با موفقیت ثبت شد.")


def save_document_in_db(document: Document):
    session = get_session()
    session.add(document)
    session.commit()


def process_user_case(message: Message, bot: TeleBot):
    tg_id = str(message.from_user.id)
    session = get_session()
    user = session.query(User).filter_by(tg_id=tg_id).first()
    if not user:
        bot.reply_to(message, "ابتدا باید توسط مدیر ثبت شوید.")
        return
    docs = session.query(Document).filter_by(client_id=user.id).order_by(Document.id.desc()).limit(10).all()
    if not docs:
        bot.reply_to(message, "شما هیچ پرونده‌ای ندارید.")
        return
    text = "\n\n-----------------------\n\n".join(
        [
            (
                f"📄 پرونده #{doc.id}\n"
                f"کوتیج: {doc.cotej_number}\n"
                f"بوکینگ: {doc.booking_number}\n"
                f"تعداد کانتینر: {doc.container_quantity}\n"
                f"وضعیت: {doc.document_status}\n"
            ) for doc in docs
        ]
    )
    bot.send_message(message.chat.id, text)


def process_search_case(message: Message, bot: TeleBot):
    if not is_admin(str(message.from_user.id)):
        bot.reply_to(message, "فقط ادمین‌ها مجاز به جستجو هستند.")
        return
    bot.reply_to(message, "چه چیزی می‌خواهید جستجو کنید؟ (cotej_number, booking_number, username, document_id)")
    bot.register_next_step_handler(message, get_search_key)


def get_search_key(message: Message, bot: TeleBot):
    keyword = message.text.strip()
    session = get_session()
    if keyword.isdigit():
        q = session.query(Document).filter(
            (Document.id == int(keyword)) |
            (Document.cotej_number == int(keyword)) |
            (Document.booking_number == int(keyword))
        ).all()
    else:
        user = session.query(User).filter_by(username=keyword.lstrip("@")).first()
        if not user:
            bot.reply_to(message, "کاربر با این یوزرنیم یافت نشد.")
            return
        q = session.query(Document).filter_by(client_id=user.id).all()
    if not q:
        bot.reply_to(message, "پرونده‌ای یافت نشد.")
        return
    for doc in q:
        bot.send_message(
            message.chat.id,
            f"📄 پرونده #{doc.id}\n"
            f"کوتیج: {doc.cotej_number}\n"
            f"بوکینگ: {doc.booking_number}\n"
            f"مالک کالا: {doc.cargo_owner}\n"
            f"مرکز تولید: {doc.production_center}\n"
            f"وضعیت سند: {doc.document_status}"
        )
