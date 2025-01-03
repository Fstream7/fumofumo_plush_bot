from random import choice
from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, KICKED, LEFT, JOIN_TRANSITION
from config import Messages


router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def chat_member_join(event: ChatMemberUpdated):
    await event.answer(Messages.new_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.new_member_sticker))


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> LEFT))
async def chat_member_left(event: ChatMemberUpdated):
    await event.answer(Messages.left_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.left_member_sticker))


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> KICKED))
async def chat_member_banned(event: ChatMemberUpdated):
    await event.answer(Messages.ban_member_message.format(user_full_name=event.new_chat_member.user.full_name))
    await event.answer_sticker(sticker=choice(Messages.ban_member_sticker))
