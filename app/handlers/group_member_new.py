from aiogram import Router
from aiogram.types import ChatMemberUpdated
from config import Messages
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION
from random import choice

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def somebody_join(event: ChatMemberUpdated):
    await event.answer(Messages.new_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.new_member_sticker))
