from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update, desc
from sqlalchemy.sql.expression import func
from .models import Fumo, QuizUsers, QuizResults


class FumoCache:
    """Keep fumo db ids in cache. So if db updated - user still can get same fumo."""
    _fumo_ids_cache: Optional[list[int]] = None

    @classmethod
    async def update_fumo_ids_cache(cls, session: AsyncSession) -> None:
        result = await session.execute(select(Fumo.id).order_by(Fumo.id))
        cls._fumo_ids_cache = [row[0] for row in result.all()]
        await session.close()

    @classmethod
    async def get_fumo_ids_cache(cls, session: AsyncSession) -> list[int]:
        if cls._fumo_ids_cache is None:
            await cls.update_fumo_ids_cache(session)
        return cls._fumo_ids_cache


async def db_add_fumo(session: AsyncSession, name: str, file_id: str, source_link: Optional[str]) -> str:
    try:
        fumo = Fumo(name=name, file_id=file_id, source_link=source_link)
        session.add(fumo)
        await session.commit()
        return f"Fumo {name} added successfully."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_get_fumo_by_id(session: AsyncSession, fumo_id: int) -> Fumo:
    fumo_ids_cache = await FumoCache.get_fumo_ids_cache(session)
    if len(fumo_ids_cache) == 0:
        return None
    fumo_list_id = fumo_ids_cache[fumo_id % len(fumo_ids_cache)]
    result = await session.execute(select(Fumo).where(Fumo.id == fumo_list_id))
    return result.scalar_one_or_none()


async def db_show_all_fumos(session: AsyncSession) -> list[Fumo]:
    result = await session.execute(select(Fumo))
    return result.scalars().all()


async def db_search_fumos_by_name(session: AsyncSession, search_pattern: str) -> Optional[list[Fumo]]:
    result = await session.execute(select(Fumo).where(Fumo.name.like(f'%{search_pattern}%')))
    return result.scalars().all()


async def db_get_fumo_by_name(session: AsyncSession, fumo_name: str) -> Optional[Fumo]:
    result = await session.execute(select(Fumo).where(Fumo.name == fumo_name))
    return result.scalar_one_or_none()


async def db_delete_fumo_by_name(session: AsyncSession, fumo_name: str) -> str:
    try:
        await session.execute(delete(Fumo).where(Fumo.name == fumo_name))
        await session.commit()
        return f"Fumo {fumo_name} deleted."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_update_fumo_name(session: AsyncSession, old_fumo_name: str, new_fumo_name: str) -> str:
    try:
        await session.execute(update(Fumo).
                              where(Fumo.name == old_fumo_name)
                              .values(name=new_fumo_name))
        await session.commit()
        return f"{new_fumo_name} name updated."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_update_fumo_file_id_by_name(session: AsyncSession, fumo_name: str, new_fumo_file_id: str) -> str:
    try:
        await session.execute(update(Fumo)
                              .where(Fumo.name == fumo_name)
                              .values(file_id=new_fumo_file_id))
        await session.commit()
        return f"{fumo_name} image updated."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_update_fumo_source_link_by_name(session: AsyncSession, fumo_name: str, new_source_link: str) -> str:
    try:
        await session.execute(update(Fumo)
                              .where(Fumo.name == fumo_name)
                              .values(source_link=new_source_link))
        await session.commit()
        return f"{fumo_name} url updated."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_update_fumo_quiz_by_name(session: AsyncSession, fumo_name: str, new_use_for_quiz: bool) -> str:
    try:
        await session.execute(update(Fumo)
                              .where(Fumo.name == fumo_name)
                              .values(use_for_quiz=new_use_for_quiz))
        await session.commit()
        return f"{fumo_name} quiz status updated."
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_get_random_fumo_for_quiz(session: AsyncSession) -> str:
    result = await session.execute(select(Fumo)
                                   .where(Fumo.use_for_quiz)
                                   .order_by(func.random())
                                   .limit(1))
    return result.scalar_one_or_none()


async def db_quiz_add_entry(
        session: AsyncSession,
        user_id: float,
        user_name: str,
        fumo_id: int,
        group_id: float
) -> str:
    """
    If record with user_id, fumo_id and group_id exist - increase fumo_count for it.
    If user name was changed - update it.
    If record not exist - create new one.
    """
    quiz_entry_result = await session.execute(select(QuizResults)
                                              .where(
        QuizResults.user_id == user_id,
        QuizResults.fumo_id == fumo_id,
        QuizResults.group_id == group_id
    ))
    quiz_entry = quiz_entry_result.scalar_one_or_none()
    if quiz_entry:
        quiz_entry.fumo_count += 1
        quiz_user_result = await session.execute(select(QuizUsers)
                                                 .where(QuizUsers.user_id == user_id))
        quiz_user = quiz_user_result.scalar_one_or_none()
        if user_name != quiz_user.user_name:
            quiz_user.user_name = user_name
    else:
        quiz_user = QuizUsers(user_id=user_id, user_name=user_name)
        session.add(quiz_user)
        quiz_entry = QuizResults(user_id=user_id, fumo_id=fumo_id, fumo_count=1, group_id=group_id)
        session.add(quiz_entry)
    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return f"Error occurred: {str(e)}"


async def db_quiz_get_records_for_user_id(session: AsyncSession, user_id: float, group_id: float) -> str:
    result = await session.execute(
        select(
            Fumo.name.label("fumo_name"),
            QuizResults.fumo_count.label("fumo_count")
        )
        .join(QuizResults, Fumo.id == QuizResults.fumo_id)
        .where(QuizResults.user_id == user_id, QuizResults.group_id == group_id)
        .order_by(desc(QuizResults.fumo_count))
    )
    return result.all()


async def db_quiz_get_leaderboard(session: AsyncSession, group_id: float) -> str:
    result = await session.execute(
        select(
            QuizResults.user_id,
            QuizUsers.user_name,
            func.sum(QuizResults.fumo_count).label("fumo_count")
        )
        .join(QuizResults, QuizUsers.user_id == QuizResults.user_id)
        .where(QuizResults.group_id == group_id)
        .group_by(QuizUsers.user_id, QuizUsers.user_name)
        .order_by(desc("fumo_count"))
        .limit(10)
    )
    return result.all()
