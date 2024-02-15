import asyncio
from functools import wraps
from typing import Callable, Optional

from aiogram import types


async def _on_media_group_received(
    media_group_id: str,
    media_data: dict,
    callback,
    *args,
    **kwargs,
):
    messages = media_data[media_group_id]
    del media_data[media_group_id]
    return await callback(messages, *args, **kwargs)


def media_group_handler(
    func: Optional[Callable] = None,
    only_album: bool = True,
    receive_timeout: float = 1.0,
    media_data: dict = {}
):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message: types.Message, *args, **kwargs):
            if only_album and message.media_group_id is None:
                raise ValueError("Not a media group message")
            elif message.media_group_id is None:
                return await handler([message], *args, **kwargs)
            event_loop = asyncio.get_running_loop()

            if message.media_group_id not in media_data:
                event_loop.call_later(
                    receive_timeout,
                    asyncio.create_task,
                    _on_media_group_received(
                        message.media_group_id, media_data, handler, *args, **kwargs
                    ))
                media_data[message.media_group_id] = []

            media_data[message.media_group_id].append(message)

        return wrapper

    if callable(func):
        return decorator(func)

    return decorator
