#!/usr/bin/env python
import asyncio
import logging
from handlers import collect_routers
from utils.commands import set_commands
from utils.scheduler import setup_scheduler
from config import Config
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy


async def start_bot(bot: Bot):
    await set_commands(bot)


async def main() -> None:
    if "postgresql+asyncpg://" in Config.DATABASE_URI.get_secret_value():
        logging.info("Using postgres DB")
    elif "sqlite+aiosqlite:///" in Config.DATABASE_URI.get_secret_value():
        logging.info("Using sqlite DB")
    logging.info(f"Using timezone {Config.TIMEZONE}")
    engine = create_async_engine(url=Config.DATABASE_URI.get_secret_value(), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.startup.register(start_bot)
    dp.include_routers(*collect_routers())
    setup_scheduler(sessionmaker(), bot, dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=Config.LOG_LEVEL)
    asyncio.run(main())
