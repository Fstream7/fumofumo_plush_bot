from aiogram.filters import BaseFilter
from aiogram.types import Message


class MessageFromChannelFilter(BaseFilter):
    """
    Filter messages from linked channel
    """

    async def __call__(self, message: Message) -> bool:
        if message.sender_chat:
            return message.sender_chat.type == "channel"
