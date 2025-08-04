def get_username(message: Message):
    username = message.text.strip().lstrip("@")
    session = get_session()
    with session() as db:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            return bot.reply_to(message, "کاربری با این یوزرنیم پیدا نشد.")
        payment_context[message.chat.id]['user_id'] = user.id
        bot.reply_to(message, "مقدار مبلغ (عدد):")
        bot.register_next_step_handler(message, get_amount)

def get_amount(message: Message):
    try:
        amount = float(message.text.strip())
    except ValueError:
        return bot.reply_to(message, "مقدار نامعتبر. لطفاً عدد وارد کنید.")
    payment_context[message.chat.id]['amount'] = amount
    bot.reply_to(message, "نوع: بدهی (`debit`) یا پرداخت (`credit`):")
    bot.register_next_step_handler(message, get_type)

def get_type(message: Message):
    ptype = message.text.strip().lower()
    if ptype not in ["debit", "credit"]:
        return bot.reply_to(message, "نوع باید 'debit' یا 'credit' باشد.")
    payment_context[message.chat.id]['type'] = ptype
    bot.reply_to(message, "توضیح اختیاری:")
    bot.register_next_step_handler(message, save_payment)

def save_payment(message: Message):
    payment_context[message.chat.id]['description'] = message.text
    data = payment_context.pop(message.chat.id)

    session = get_session()
    with session() as db:
        payment = Payment(**data)
        db.add(payment)
        db.commit()
    bot.reply_to(message, "ثبت پرداخت با موفقیت انجام شد.")


def balance_for_admin(message: Message):
    session = get_session()
    with session() as db:
        username = message.text.strip().lstrip("@")
        user = db.query(User).filter_by(username=username).first()
        if not user:
            return bot.reply_to(message, "کاربر پیدا نشد.")
        show_balance(bot, message.chat.id, user.id)


def show_balance(bot, chat_id, user_id):
    session = get_session()
    with session() as db:
        from models.payment import Payment
        payments = db.query(Payment).filter_by(user_id=user_id).all()
        if not payments:
            return bot.send_message(chat_id, "تراکنشی ثبت نشده است.")

        total = 0
        lines = []
        for p in payments:
            sign = "+" if p.type == "credit" else "-"
            amount = float(p.amount)
            lines.append(f"{p.created_at.date()} | {p.type} | {amount} | {p.description or '-'}")
            total += amount if p.type == "credit" else -amount

        text = "\n".join(lines)
        summary = f"\n\n💰 مانده نهایی: {total:.2f} تومان"
        bot.send_message(chat_id, f"📋 لیست تراکنش‌ها:\n{text}{summary}")

