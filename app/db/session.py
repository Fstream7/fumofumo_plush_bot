from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import logging
from config import Config

logging.basicConfig(level=Config.LOG_LEVEL)

if "postgresql+asyncpg://" in Config.DATABASE_URI.get_secret_value():
    logging.info("Using postgres DB")
elif "sqlite+aiosqlite:///" in Config.DATABASE_URI.get_secret_value():
    logging.info("Using sqlite DB")
engine = create_async_engine(url=Config.DATABASE_URI.get_secret_value(), echo=True)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
