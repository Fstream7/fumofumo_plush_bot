from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def quiz_buttons(fumos_list: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for fumo_name in fumos_list:
        keyboard.button(text=fumo_name, callback_data=fumo_name)
    keyboard.adjust(2)
    return keyboard.as_markup()
