def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def handle_start(message: Message):
        tg_id = str(message.from_user.id)
        username = message.from_user.username

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