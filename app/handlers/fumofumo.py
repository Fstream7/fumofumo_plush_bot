from aiogram.filters import Command
from aiogram import Router, types
from config import Messages, Config
from random import choice
from db.requests import db_get_fumo_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode
import hashlib

router = Router()


@router.message(Command("fumo"))
async def fumo(message: types.Message) -> None:
    await message.reply(f"Fumo {choice(['ᗜᴗᗜ', 'ᗜˬᗜ', 'ᗜ˰ᗜ', 'ᗜ‿ᗜ', 'ᗜ_ᗜ', 'ᗜωᗜ'])}")


@router.message(Command("fumofumo"))
async def fumofumo(message: types.Message, session: AsyncSession) -> None:
    fumo_string = f"{message.from_user.id}_{message.date.strftime('%Y%m%d')}"
    fumo_hash = hashlib.blake2b(fumo_string.encode(),
                                digest_size=8,
                                salt=str.encode(Config.HASH_SALT.get_secret_value())
                                ).hexdigest()
    fumo_id = int(fumo_hash, 16)
    fumo = await db_get_fumo_by_id(session, fumo_id)
    await message.reply_photo(
        photo=fumo.file_id,
        caption=Messages.fumofumo_message.format(fumo=f"[{fumo.name}]({fumo.source_link})"),
        parse_mode=ParseMode.MARKDOWN_V2)
