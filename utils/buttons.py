from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def create_glass_buttons(buttons_dict: list):
    keyboard = InlineKeyboardMarkup()
    for row_dict in buttons_dict:
        row_buttons = []
        for text, callback_data in row_dict.items():
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            row_buttons.append(button)
        keyboard.row(*row_buttons)

    return keyboard


def create_reply_buttons(buttons_list: list):
    keyboard = []
    for text in buttons_list:
        button = KeyboardButton(text)
        keyboard.append(button)
    return ReplyKeyboardMarkup(one_time_keyboard=True, selective=True).add(*keyboard)
