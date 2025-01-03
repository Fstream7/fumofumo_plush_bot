from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextIsCommandFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            return message.text.startswith("/")
