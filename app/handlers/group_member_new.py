from aiogram import Router, F, types
from config import Messages
from random import choice

router = Router()


@router.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(Messages.new_member_message.format(user_full_name=user.full_name))
        await message.answer_sticker(sticker=choice(Messages.new_member_sticker))
