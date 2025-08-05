from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_buttons_from_list(info: list):
    keyboard = InlineKeyboardMarkup()

    for row_dict in info:
        row_buttons = []
        for text, callback_data in row_dict.items():
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            row_buttons.append(button)
        keyboard.row(*row_buttons)

    return keyboard

