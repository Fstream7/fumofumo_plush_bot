import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextIsLinkFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        url_pattern = re.compile(
            r'^(https?://)?'
            r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
            r'(/.*)?$'
        )
        return bool(url_pattern.match(message.text))
