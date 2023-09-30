#!/usr/bin/env python
from config import Config
from handlers import start, propose, get_media_id, members_new, members_left
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio
import logging
from aiogram import Bot, Dispatcher


async def main() -> None:
    engine = create_async_engine(url=str(Config.DATABASE_URI), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
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
