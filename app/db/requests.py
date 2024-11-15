from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .models import Fumo
from sqlalchemy import select, delete
from typing import Optional

_fumo_ids_cache = None


async def db_add_fumo(session: AsyncSession, name: str, file_id: str) -> str:
    try:
        fumo = Fumo(name=name, file_id=file_id)
        session.add(fumo)
        await session.commit()
        return f"Fumo {name} added successfully."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def update_fumo_ids_cache(session: AsyncSession) -> None:
    global _fumo_ids_cache
    result = await session.execute(select(Fumo.id).order_by(Fumo.id))
    _fumo_ids_cache = [row[0] for row in result.all()]


async def db_get_fumo_by_id(session: AsyncSession, id: int) -> Fumo:
    if _fumo_ids_cache is None:
        await update_fumo_ids_cache(session)
    fumo_list_id = _fumo_ids_cache[id % len(_fumo_ids_cache)]
    result = await session.execute(select(Fumo).where(Fumo.id == fumo_list_id))
    return result.scalar_one_or_none()


async def db_show_all_fumos(session: AsyncSession) -> list[Fumo]:
    result = await session.execute(select(Fumo))
    return result.scalars().all()


async def db_search_fumos_by_name(session: AsyncSession, search_pattern: str) -> Optional[Fumo]:
    result = await session.execute(select(Fumo).where(Fumo.name.like(f'%{search_pattern}%')))
    return result.scalars().all()


async def db_delete_fumo_by_name(session: AsyncSession, fumo_name: str) -> str:
    try:
        await session.execute(delete(Fumo).where(Fumo.name == fumo_name))
        await session.commit()
        return f"Fumo {fumo_name} deleted."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"
