#!/usr/bin/env python
from handlers import get_id, group_member_left, group_member_new, private_admin, private_users, start
from handlers import group_member_banned
from config import Config
import asyncio
import logging
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(get_id.router)
    dp.include_router(private_admin.router)
    dp.include_router(private_users.router)
    dp.include_router(group_member_new.router)
    dp.include_router(group_member_left.router)
    dp.include_router(group_member_banned.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=Config.LOG_LEVEL)
    asyncio.run(main())
