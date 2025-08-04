from telebot.types import Message, Document
from models.base import get_session
from models.files import File
from models.document import Document as CaseDocument
from config import ARCHIVE_CHANNEL_ID
from utils.auth import is_admin


def ask_doc_id(message: Message):
    try:
        doc_id = int(message.text.strip())
        session = get_session()
        with session() as db:
            doc = db.query(CaseDocument).filter_by(id=doc_id).first()
            if not doc:
                return bot.reply_to(message, "پرونده‌ای با این شماره یافت نشد.")
            upload_context[message.chat.id]['document_id'] = doc_id
    except ValueError:
        return bot.reply_to(message, "شماره پرونده باید عدد باشد.")

    bot.reply_to(message, "اکنون فایل خود را ارسال کنید:")
    bot.register_next_step_handler(message, receive_file)

def receive_file(message: Message):
    if not message.document:
        return bot.reply_to(message, "لطفاً فایل ارسال کنید.")

    upload_context[message.chat.id]['file'] = message.document
    upload_context[message.chat.id]['file_id'] = message.document.file_id
    bot.reply_to(message, "نوع فایل را وارد کنید (مثلاً: Invoice، Packing List و ...):")
    bot.register_next_step_handler(message, get_file_type)

def get_file_type(message: Message):
    upload_context[message.chat.id]['file_type'] = message.text
    bot.reply_to(message, "توضیح اختیاری برای فایل:")
    bot.register_next_step_handler(message, get_description)

def get_description(message: Message):
    data = upload_context.pop(message.chat.id)
    description = message.text
    file = data['file']

    # ارسال فایل به کانال آرشیو
    sent = bot.send_document(
        ARCHIVE_CHANNEL_ID,
        file.file_id,
        caption=f"📎 فایل مرتبط با پرونده #{data['document_id']}\nنوع: {data['file_type']}"
    )

    # ذخیره در دیتابیس
    session = get_session()
    with session() as db:
        file_record = File(
            document_id=data['document_id'],
            url_link=f"https://t.me/c/{str(ARCHIVE_CHANNEL_ID).lstrip('-100')}/{sent.message_id}",
            file_type=data['file_type'],
            description=description,
            telegram_msg_id=sent.message_id,
            telegram_chat_id=sent.chat.id,
        )
        db.add(file_record)
        db.commit()

    bot.reply_to(message, "فایل با موفقیت ذخیره شد.")


def process_doc_id(message: Message):
    try:
        doc_id = int(message.text.strip())
    except ValueError:
        return bot.reply_to(message, "فرمت عددی صحیح نیست.")

    session = get_session()
    with session() as db:
        doc = db.query(Document).filter_by(id=doc_id).first()
        if not doc:
            return bot.reply_to(message, "پرونده‌ای با این شماره یافت نشد.")

        user = db.query(User).filter_by(tg_id=str(message.from_user.id)).first()
        if not user:
            return bot.reply_to(message, "کاربری شما در سیستم ثبت نشده است.")

        if user.role != "admin" and doc.client_id != user.id:
            return bot.reply_to(message, "شما مجاز به دیدن این پرونده نیستید.")

        files = db.query(File).filter_by(document_id=doc_id).all()
        if not files:
            return bot.reply_to(message, "فایلی برای این پرونده یافت نشد.")

        for f in files:
            caption = f"📎 نوع فایل: {f.file_type}\n📝 توضیح: {f.description or '---'}"
            bot.send_message(message.chat.id, f"{caption}\n🔗 لینک: {f.url_link}")
