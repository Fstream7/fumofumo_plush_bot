from config import Config
from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.id == Config.ADMIN_CHAT_ID:
            return True
        else:
            return False
