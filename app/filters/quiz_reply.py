from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import Bot


class QuizReplyFilter(BaseFilter):
    """
    Here we check that reply to quiz was to bot message
    """

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if message.reply_to_message:
            return message.reply_to_message.from_user.id == bot.id
