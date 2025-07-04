from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import Bot
from config import Messages


class QuizFilter(BaseFilter):
    """
    Limit quiz commands with quiz group
    """

    async def __call__(self, message: Message, bot: Bot) -> bool:
        return any(chat["id"] == message.chat.id for chat in Messages.quiz_chats)


class QuizReplyFilter(BaseFilter):
    """
    Here we check that reply to quiz was to bot message
    """

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if message.reply_to_message:
            return message.reply_to_message.from_user.id == bot.id
