def register_handlers(bot):
    @bot.message_handler(commands=['add_client'])
    def start_add_client(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "شما ادمین نیستید.")
        bot.reply_to(message, "نام مشتری را وارد کنید:")
        user_register_data[message.chat.id] = {}
        bot.register_next_step_handler(message, get_name)


def register_handlers(bot):
    @bot.message_handler(commands=["client_stats"])
    def handle_client_stats(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "فقط ادمین‌ها مجاز به مشاهده آمار هستند.")
        bot.reply_to(message, "یوزرنیم مشتری را وارد کنید:")
        bot.register_next_step_handler(message, process_username)

