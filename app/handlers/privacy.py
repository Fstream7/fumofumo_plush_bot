from aiogram.filters import Command
from aiogram import Router, types
from config import Messages

router = Router()


@router.message(Command("privacy"))
async def cmd_privacy(message: types.Message) -> None:
    await message.reply(Messages.privacy)
