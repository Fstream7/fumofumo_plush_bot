from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def edit_buttons() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="edit",
        callback_data="edit_fumo"
    )
    keyboard.button(
        text="delete",
        callback_data="delete_fumo"
    )
    return keyboard.as_markup()


def confirm_buttons() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="yes",
        callback_data="confirm_delete"
    )
    keyboard.button(
        text="no",
        callback_data="cancel_delete"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
