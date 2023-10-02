from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import media_users

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        f"Hello {message.from_user.full_name}! Chat id {message.from_user.id}"
    )
    await session.merge(media_users(user_id=message.from_user.id, username=message.from_user.username, date_added=message.date))
    await session.commit()
