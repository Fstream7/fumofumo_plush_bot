from aiogram import Router, F
from aiogram import types
from config import Config
from random import choice

router = Router()


@router.message(F.left_chat_member)
async def somebody_leaved(message: types.Message):
    await message.reply(
        f"Fumo fren no more, goodbye {message.left_chat_member.full_name}"
    )
    await message.answer_sticker(sticker=choice(Config.GOODBYE_STIKERS))
