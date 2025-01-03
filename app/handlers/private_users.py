from typing import List
from random import choice
from aiogram import Router, F, types, Bot
from aiogram.methods import ForwardMessages
from aiogram.filters import Command, invert_f
from config import Config, Messages
from filters.chat_type import ChatTypeFilter
from filters.admin import AdminFilter
from decorators.media_group_handler import media_group_handler


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["private"]), invert_f(AdminFilter()))


@router.message(Command("propose"))
async def propose(message: types.Message) -> None:
    await message.reply(
        "Send me fumo images and I will forward them for admins to post on channel.\n"
        "If you do not want your account to be viewed on forwarding to channel, then "
        "disable link for forwarding in Telegram privacy settings or write in "
        "the message that you want to remain anonymous.\n"
        "`/propose` command is deprecated and dont need anymore, just send fumo images to bot"
    )


@router.message(F.media_group_id, F.content_type.in_({'photo', 'video', 'audio', 'document'}))
@media_group_handler
async def media_group(messages: List[types.Message], bot: Bot) -> None:
    await bot.send_message(
        Config.ADMIN_CHAT_ID,
        (
            f"New message from {messages[-1].from_user.full_name} "
            f"@{messages[-1].from_user.username} "
            f"({messages[-1].from_user.id})"
        )
    )
    unsorted_message_ids = [message.message_id for message in messages]
    await bot(
        ForwardMessages(
            chat_id=Config.ADMIN_CHAT_ID,
            from_chat_id=messages[-1].chat.id,
            message_ids=sorted(unsorted_message_ids)
        )
    )
    await messages[-1].answer(Messages.thanks_message.format(user_full_name=messages[-1].from_user.full_name))
    await messages[-1].answer_sticker(sticker=choice(Messages.thanks_sticker))


@router.message()
async def process_propose(message: types.Message, bot: Bot) -> None:
    await bot.send_message(
        Config.ADMIN_CHAT_ID,
        (
            f"New message from {message.from_user.full_name} "
            f"@{message.from_user.username} "
            f"({message.from_user.id})"
        )
    )
    await message.forward(Config.ADMIN_CHAT_ID)
    await message.answer(Messages.thanks_message.format(user_full_name=message.from_user.full_name))
    await message.answer_sticker(sticker=choice(Messages.thanks_sticker))
