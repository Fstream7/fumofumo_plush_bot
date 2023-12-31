from aiogram import Router, F
from aiogram.types import Message
from filters.chat_type import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["private"]))


@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer(f"Sticker file_id {message.sticker.file_id}")


@router.message(F.photo)
async def message_with_photo(message: Message):
    await message.answer(f"Photo file_id {message.photo[-1].file_id}")


@router.message(F.animation)
async def message_with_animation(message: Message):
    await message.answer(f"Animation file_id {message.animation.file_id}")
