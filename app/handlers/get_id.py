from aiogram.filters import Command
from aiogram import Router, types

router = Router()


@router.message(Command("id"))
async def return_id(message: types.Message) -> None:
    await message.reply(f"Chat id  {message.chat.id}")


@router.message(Command("fumo"))
async def fumo(message: types.Message) -> None:
    await message.reply("Fumo ᗜᴗᗜ")
