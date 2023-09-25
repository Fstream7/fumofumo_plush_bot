from aiogram import Router, F
from aiogram import types
from config import Config
from random import choice

router = Router()


@router.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Hello, {user.full_name}")
        await message.answer_sticker(sticker=choice(Config.HELLO_STIKERS))
