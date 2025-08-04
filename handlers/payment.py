def register_handlers(bot):
    @bot.message_handler(commands=["add_payment"])
    def handle_add_payment(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "فقط ادمین‌ها مجاز به ثبت پرداخت هستند.")
        bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
        payment_context[message.chat.id] = {}
        bot.register_next_step_handler(message, get_username)


def register_handlers(bot):
    @bot.message_handler(commands=["balance"])
    def handle_balance(message: Message):
        session = get_session()
        with session() as db:
            if is_admin(str(message.from_user.id)):
                bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
                bot.register_next_step_handler(message, balance_for_admin)
            else:
                user = db.query(User).filter_by(tg_id=str(message.from_user.id)).first()
                if not user:
                    return bot.reply_to(message, "شما ثبت نشده‌اید.")
                return show_balance(bot, message.chat.id, user.id)