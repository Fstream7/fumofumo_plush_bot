#!/usr/bin/env python
from config import Config
from handlers import start, propose, get_media_id, members_new, members_left
import asyncio
import logging
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(token=Config.TOKEN)
    dp = Dispatcher()
    # await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(start.router)
    dp.include_router(propose.router)
    dp.include_router(members_new.router)
    dp.include_router(members_left.router)
    dp.include_router(get_media_id.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=Config.LOG_LEVEL)
    asyncio.run(main())
