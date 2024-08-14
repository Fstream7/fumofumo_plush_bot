from aiogram import Router
from aiogram.types import ChatMemberUpdated
from config import Messages
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, RESTRICTED, KICKED
from random import choice

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> (RESTRICTED | KICKED)))
async def somebody_banned(event: ChatMemberUpdated):
    await event.answer(Messages.ban_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.ban_member_sticker))
