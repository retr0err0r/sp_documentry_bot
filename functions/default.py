def ask_for_role(message: Message, db, user):
    text = message.text.strip()
    if text == ADMIN_KEY:
        user.role = "admin"
        db.commit()
        bot.reply_to(message, "نقش شما به عنوان ادمین تنظیم شد.")
    else:
        user.role = "client"
        db.commit()
        bot.reply_to(message, "نقش شما به عنوان مشتری تنظیم شد.")
