from aiogram import Router
from aiogram.types import ChatMemberUpdated
from config import Messages
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, LEFT
from random import choice

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> LEFT))
async def somebody_leaved(event: ChatMemberUpdated):
    await event.answer(Messages.left_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.left_member_sticker))
