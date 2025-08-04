def get_name(message: Message):
    user_register_data[message.chat.id]['name'] = message.text
    bot.reply_to(message, "یوزرنیم تلگرام مشتری را وارد کنید:")
    bot.register_next_step_handler(message, get_username)

def get_username(message: Message):
    user_register_data[message.chat.id]['username'] = message.text
    bot.reply_to(message, "شماره تلفن مشتری را وارد کنید:")
    bot.register_next_step_handler(message, save_user)

def save_user(message: Message):
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


def process_username(message: Message):
    username = message.text.strip().lstrip("@")
    session = get_session()
    with session() as db:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            return bot.reply_to(message, "کاربری با این یوزرنیم پ_
