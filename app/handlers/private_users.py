from aiogram import Router, F, types, Bot
from aiogram.methods import ForwardMessages
from config import Config
from filters.chat_type import ChatTypeFilter
from typing import List
from decorators.media_group_handler import media_group_handler
from config import Messages
from random import choice

router = Router()


@router.message(
    ChatTypeFilter(chat_type=["private"]),
    F.media_group_id,
    F.content_type.in_({'photo', 'video', 'audio', 'document'}))
@media_group_handler
async def media_group(messages: List[types.Message], bot: Bot) -> None:
    await bot.send_message(
        Config.ADMIN_CHAT_ID,
        f"New message from {messages[-1].from_user.full_name} @{messages[-1].from_user.username}({messages[-1].from_user.id})"
    )
    await bot(ForwardMessages(chat_id=Config.ADMIN_CHAT_ID,
                              from_chat_id=messages[-1].chat.id,
                              message_ids=[message.message_id for message in messages]))
    await messages[-1].answer(Messages.thanks_message.format(user_full_name=messages[-1].from_user.full_name))
    await messages[-1].answer_sticker(sticker=choice(Messages.thanks_sticker))


@router.message(ChatTypeFilter(chat_type=["private"]))
async def process_propose(message: types.Message, bot: Bot) -> None:
    await bot.send_message(
        Config.ADMIN_CHAT_ID,
        f"New message from {message.from_user.full_name} @{message.from_user.username}({message.from_user.id})"
    )
    await message.forward(Config.ADMIN_CHAT_ID)
    await message.answer(Messages.thanks_message.format(user_full_name=message.from_user.full_name))
    await message.answer_sticker(sticker=choice(Messages.thanks_sticker))
