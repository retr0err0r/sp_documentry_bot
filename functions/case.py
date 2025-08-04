def get_username(message: Message):
    session = get_session()
    with session() as db:
        username = message.text.strip().lstrip("@")
        user = db.query(User).filter_by(username=username).first()
        if not user:
            return bot.reply_to(message, "مشتری یافت نشد.")
        case_data[message.chat.id]['client_id'] = user.id
        bot.reply_to(message, "شماره کوتیج را وارد کنید:")
        bot.register_next_step_handler(message, get_cotej)

def get_cotej(message: Message):
    case_data[message.chat.id]['cotej_number'] = message.text
    bot.reply_to(message, "شماره بوکینگ را وارد کنید:")
    bot.register_next_step_handler(message, get_booking)

def get_booking(message: Message):
    case_data[message.chat.id]['booking_number'] = message.text
    bot.reply_to(message, "تعداد کانتینر:")
    bot.register_next_step_handler(message, get_container_quantity)

def get_container_quantity(message: Message):
    case_data[message.chat.id]['container_quantity'] = int(message.text)
    bot.reply_to(message, "سایز کانتینر:")
    bot.register_next_step_handler(message, get_container_size)

def get_container_size(message: Message):
    case_data[message.chat.id]['container_size'] = message.text
    bot.reply_to(message, "نوع کالا:")
    bot.register_next_step_handler(message, get_goods_type)

def get_goods_type(message: Message):
    case_data[message.chat.id]['goods_type'] = message.text
    bot.reply_to(message, "تاریخ تخصیص (YYYY-MM-DD):")
    bot.register_next_step_handler(message, get_assignment_date)

def get_assignment_date(message: Message):
    case_data[message.chat.id]['assignment_date'] = message.text
    bot.reply_to(message, "شرکت کشتیرانی:")
    bot.register_next_step_handler(message, get_shipping_company)

def get_shipping_company(message: Message):
    case_data[message.chat.id]['shipping_company'] = message.text
    bot.reply_to(message, "مالک کالا:")
    bot.register_next_step_handler(message, get_cargo_owner)

def get_cargo_owner(message: Message):
    case_data[message.chat.id]['cargo_owner'] = message.text
    bot.reply_to(message, "مرکز تولید:")
    bot.register_next_step_handler(message, get_production_center)

def get_production_center(message: Message):
    case_data[message.chat.id]['production_center'] = message.text
    bot.reply_to(message, "وضعیت سند:")
    bot.register_next_step_handler(message, get_document_status)

def get_document_status(message: Message):
    case_data[message.chat.id]['document_status'] = message.text
    bot.reply_to(message, "وضعیت پرداخت:")
    bot.register_next_step_handler(message, get_payment_status)

def get_payment_status(message: Message):
    case_data[message.chat.id]['payment_status'] = message.text

    # ذخیره نهایی در DB
    session = get_session()
    with session() as db:
        data = case_data.pop(message.chat.id)
        doc = Document(**data)
        db.add(doc)
        db.commit()

    bot.reply_to(message, "پرونده با موفقیت ثبت شد.")




def get_search_key(message: Message):
    keyword = message.text.strip()
    session = get_session()
    with session() as db:
        # اگر عدد بود → فرض می‌کنیم document_id یا cotej/booking
        if keyword.isdigit():
            q = db.query(Document).filter(
                (Document.id == int(keyword)) |
                (Document.cotej_number == int(keyword)) |
                (Document.booking_number == int(keyword))
            ).all()
        else:
            user = db.query(User).filter_by(username=keyword.lstrip("@")).first()
            if not user:
                return bot.reply_to(message, "کاربر با این یوزرنیم یافت نشد.")
            q = db.query(Document).filter_by(client_id=user.id).all()

        if not q:
            return bot.reply_to(message, "پرونده‌ای یافت نشد.")

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
