from telebot import TeleBot
from telebot.types import Message

from config import ARCHIVE_CHANNEL_ID
from models import get_session, File, User, Document

upload_context = {}


def process_upload_file(message: Message, bot: TeleBot):
    bot.reply_to(message, "شماره پرونده (document_id) را وارد کنید:")
    upload_context[message.chat.id] = {}
    bot.register_next_step_handler(message, ask_doc_id, bot)


def ask_doc_id(message: Message, bot: TeleBot):
    try:
        doc_id = int(message.text.strip())
        session = get_session()
        doc = session.query(Document).filter_by(id=doc_id).first()
        if not doc:
            bot.reply_to(message, "پرونده‌ای با این شماره یافت نشد.")
            return
        upload_context[message.chat.id]['document_id'] = doc_id
    except ValueError:
        bot.reply_to(message, "شماره پرونده باید عدد باشد.")
        return

    bot.reply_to(message, "اکنون فایل خود را ارسال کنید:")
    bot.register_next_step_handler(message, receive_file, bot)


def receive_file(message: Message, bot: TeleBot):
    if not message.document:
        bot.reply_to(message, "لطفاً فایل ارسال کنید.")
        return

    upload_context[message.chat.id]['file'] = message.document
    upload_context[message.chat.id]['file_id'] = message.document.file_id
    bot.reply_to(message, "توضیح اختیاری برای فایل:")
    bot.register_next_step_handler(message, get_description, bot)


def get_description(message: Message, bot: TeleBot):
    data = upload_context.pop(message.chat.id)
    description = message.text
    file = data['file']

    # ارسال فایل به کانال آرشیو
    doc_id = data.get('document_id', "نامشخص")
    file_type = data.get('file_type', "نامشخص")
    sent = bot.send_document(
        ARCHIVE_CHANNEL_ID,
        file.file_id,
        caption=f"📎 فایل مرتبط با پرونده #{doc_id}\nنوع: {file_type}"
    )

    # ذخیره در دیتابیس
    session = get_session()
    file_record = File(
        document_id=data['document_id'],
        url_link=f"https://t.me/c/{str(ARCHIVE_CHANNEL_ID).lstrip('-100')}/{sent.message_id}",
        file_type=data.get('file_type', "N/A"),
        description=description,
        telegram_msg_id=sent.message_id,
        telegram_chat_id=sent.chat.id,
    )
    session.add(file_record)
    session.commit()

    bot.reply_to(message, "فایل با موفقیت ذخیره شد.")


def process_show_files(message: Message, bot: TeleBot):
    bot.reply_to(message, "شماره پرونده (document_id) را وارد کنید:")
    bot.register_next_step_handler(message, process_doc_id, bot)


def process_doc_id(message: Message, bot: TeleBot):
    try:
        doc_id = int(message.text.strip())
    except ValueError:
        bot.reply_to(message, "فرمت عددی صحیح نیست.")
        return
    session = get_session()
    doc = session.query(Document).filter_by(id=doc_id).first()
    if not doc:
        bot.reply_to(message, "پرونده‌ای با این شماره یافت نشد.")
        return
    user = session.query(User).filter_by(tg_id=str(message.from_user.id)).first()
    if not user:
        bot.reply_to(message, "کاربری شما در سیستم ثبت نشده است.")
        return
    if user.role != "admin" and doc.client_id != user.id:
        bot.reply_to(message, "شما مجاز به دیدن این پرونده نیستید.")
        return
    files = session.query(File).filter_by(document_id=doc_id).all()
    if not files:
        bot.reply_to(message, "فایلی برای این پرونده یافت نشد.")
        return
    for f in files:
        caption = f"📎 نوع فایل: {f.file_type}\n📝 توضیح: {f.description or '---'}"
        bot.send_message(message.chat.id, f"{caption}\n🔗 لینک: {f.url_link}")
