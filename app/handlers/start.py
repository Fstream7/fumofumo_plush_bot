from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        f"Hello {message.from_user.full_name}! Chat id {message.from_user.id}"
    )
