import pytest
from aiogram import Dispatcher
from tests.mocked_bot import MockedBot
from app.handlers import start
from app.db.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


@pytest.fixture(scope="session")
def bot() -> MockedBot:
    return MockedBot()


@pytest.fixture(scope="session")
def dp() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    return dispatcher


@pytest.fixture(scope="session")
def async_engine():
    """
    Create async engine for tests
    aiosqlite cant work well with in-memory db, so create db file
    """
    engine = create_async_engine("sqlite+aiosqlite:///tests/testdb.sqlite", echo=False)
    try:
        yield engine
    finally:
        engine.sync_engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False)
    async with sessionmaker() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
