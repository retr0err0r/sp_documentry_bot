def register_handlers(bot):
    @bot.message_handler(commands=["upload_file"])
    def handle_upload_file(message: Message):
        if not is_admin(str(message.from_user.id)):
            return bot.reply_to(message, "دسترسی محدود به ادمین‌هاست.")
        bot.reply_to(message, "شماره پرونده (document_id) را وارد کنید:")
        upload_context[message.chat.id] = {}
        bot.register_next_step_handler(message, ask_doc_id)


def register_handlers(bot):
    @bot.message_handler(commands=["show_files"])
    def handle_show_files(message: Message):
        bot.reply_to(message, "شماره پرونده (document_id) را وارد کنید:")
        bot.register_next_step_handler(message, process_doc_id)
