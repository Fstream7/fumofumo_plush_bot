#!/usr/bin/env python
from config import Config
from handlers import start, propose
import asyncio
import logging
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(token=Config.TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(propose.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=Config.LOG_LEVEL)
    asyncio.run(main())
