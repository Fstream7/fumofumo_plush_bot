from aiogram import Router, F, types
from config import Messages
from random import choice

router = Router()


@router.message(F.left_chat_member)
async def somebody_leaved(message: types.Message):
    await message.answer(Messages.left_member_message.format(user_full_name=message.left_chat_member.full_name))
    await message.answer_sticker(sticker=choice(Messages.left_member_sticker))
