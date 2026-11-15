from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import sessionmaker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session
