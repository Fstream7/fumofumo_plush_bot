#!/usr/bin/env python
from handlers import get_id, fumofumo, group_member_left, group_member_new, private_admin, private_users, start
from handlers import group_member_banned
from utils.commands import set_commands_for_admins
from utils.scheduler import setup_scheduler
from config import Config
import asyncio
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging
from aiogram import Bot, Dispatcher


async def start_bot(bot: Bot):
    await set_commands_for_admins(bot)


async def main() -> None:
    if "postgresql+asyncpg://" in Config.DATABASE_URI.get_secret_value():
        logging.info("Using postgres DB")
    elif "sqlite+aiosqlite:///" in Config.DATABASE_URI.get_secret_value():
        logging.info("Using sqlite DB")
    engine = create_async_engine(url=Config.DATABASE_URI.get_secret_value(), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.startup.register(start_bot)
    dp.include_router(start.router)
    dp.include_router(get_id.router)
    dp.include_router(fumofumo.router)
    dp.include_router(private_admin.router)
    dp.include_router(private_users.router)
    dp.include_router(group_member_new.router)
    dp.include_router(group_member_left.router)
    dp.include_router(group_member_banned.router)
    setup_scheduler(sessionmaker())
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=Config.LOG_LEVEL)
    asyncio.run(main())
