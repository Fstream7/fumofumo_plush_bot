from aiogram import Router, F, types
from aiogram.types import Message
from filters.admin import AdminFilter
from filters.media_with_caption import MediaWithCaptionFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from db.requests import db_add_fumo, update_fumo_ids_cache, db_show_all_fumos
from aiogram.filters import and_f

router = Router()


class Form(StatesGroup):
    name = State()


@router.message(Command("get_stickers_id"), AdminFilter())
async def cmd_start_get_stickers(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Send me a stickers, I will write their file_id. \nSend /cancel to stop")


@router.message(Form.name, F.sticker)
async def message_with_sticker(message: Message):
    await message.answer(f"Sticker file_id {message.sticker.file_id}")


@router.message(Command("add_fumo"), AdminFilter())
async def cmd_start_get_images(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Send me a fumo image and name, I wil add it to database \nSend /cancel to stop")


@router.message(Form.name, and_f(F.photo, MediaWithCaptionFilter()))
async def add_fumo(message: Message, session: AsyncSession):
    fumo_name = message.caption
    fumo_file_id = message.photo[0].file_id
    result = await db_add_fumo(session, fumo_name, fumo_file_id)
    await message.reply(result)
    await update_fumo_ids_cache(session)


@router.message(Form.name, Command("cancel"))
@router.message(Form.name, F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancelled.")


@router.message(Command("list_fumos"), AdminFilter())
async def show_all_fumos(message: types.Message, session: AsyncSession) -> None:
    fumos = await db_show_all_fumos(session)
    for fumo in fumos:
        await message.answer_photo(
            photo=fumo.file_id,
            caption=fumo.name)
