from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def quiz_buttons(fumos_list: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for fumo_name in fumos_list:
        keyboard.button(text=fumo_name, callback_data=fumo_name)
    keyboard.adjust(2)
    return keyboard.as_markup()


def stop_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Stop", callback_data="stop")
    return keyboard.as_markup(resize_keyboard=True)


def continue_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Continue", callback_data="continue")
    return keyboard.as_markup(resize_keyboard=True)
