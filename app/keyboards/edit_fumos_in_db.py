from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def edit_buttons(enable_for_quiz_status: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if enable_for_quiz_status:
        enable_for_quiz_emoji = "✅"
    else:
        enable_for_quiz_emoji = "🚫"
    keyboard.button(
        text="edit name",
        callback_data="edit_fumo_name"
    )
    keyboard.button(
        text="edit link",
        callback_data="edit_fumo_source_link"
    )
    keyboard.button(
        text="replace image",
        callback_data="edit_fumo_image"
    )
    keyboard.button(
        text=(f"quiz {enable_for_quiz_emoji}"),
        callback_data="toggle_fumo_for_quiz",
    )
    keyboard.button(
        text="delete",
        callback_data="delete_fumo"
    )
    keyboard.adjust(2)
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
