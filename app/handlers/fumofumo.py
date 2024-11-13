from aiogram.filters import Command
from aiogram import Router, types
from config import Messages
from random import choice

router = Router()


@router.message(Command("fumo"))
async def fumo(message: types.Message) -> None:
    await message.reply(f"Fumo {choice(['ᗜᴗᗜ', 'ᗜˬᗜ', 'ᗜ˰ᗜ', 'ᗜ‿ᗜ', 'ᗜ_ᗜ', 'ᗜωᗜ'])}")


@router.message(Command("fumofumo"))
async def fumofumo(message: types.Message) -> None:
    fumo_id = message.from_user.id + int(message.date.strftime('%Y%m%d'))
    fumo_list_id = fumo_id % len(Messages.fumofumo_fumos)
    await message.reply_photo(
        photo=Messages.fumofumo_fumos[fumo_list_id]['picture_id'],
        caption=Messages.fumofumo_message.format(fumo=Messages.fumofumo_fumos[fumo_list_id]['name']))
