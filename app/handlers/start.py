from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from config import Messages

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(Messages.welcome_message.format(user_full_name=message.from_user.full_name))
