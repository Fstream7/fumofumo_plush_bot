from aiogram import Router, F, types
from aiogram.types import Message
from filters.admin import AdminFilter
from filters.media_with_caption import MediaWithCaptionFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession
from db.requests import db_add_fumo, update_fumo_ids_cache, db_show_all_fumos, db_search_fumos_by_name
from db.requests import db_delete_fumo_by_name
from aiogram.filters import and_f
from keyboards.edit_fumos_in_db import edit_buttons, confirm_buttons

router = Router()


class Form(StatesGroup):
    get_stickers_id = State()
    add_fumo = State()
    remove_fumo = State()
    edit_fumo = State()


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancelled.")


@router.message(Command("get_stickers_id"), AdminFilter())
async def cmd_start_get_stickers(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.get_stickers_id)
    await message.answer("Send me a stickers, I will write their file_id. \nSend /cancel to stop")


@router.message(Form.get_stickers_id, F.sticker)
async def message_with_sticker(message: Message):
    await message.answer(f"Sticker file_id {message.sticker.file_id}")


@router.message(Command("add_fumo"), AdminFilter())
async def cmd_add_fumo(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.add_fumo)
    await message.answer("Send me a fumo image and name, I wil add it to database \nSend /cancel to stop")


@router.message(Form.add_fumo, and_f(F.photo, MediaWithCaptionFilter()))
async def add_fumo(message: Message, session: AsyncSession):
    fumo_name = message.caption
    fumo_file_id = message.photo[0].file_id
    result = await db_add_fumo(session, fumo_name, fumo_file_id)
    await message.reply(result)
    await update_fumo_ids_cache(session)


@router.message(Form.add_fumo)
async def add_fumo_invalid_input(message: Message):
    await message.reply("Please send fumo photo with caption. \nSend /cancel to cancel")


@router.message(Command("list_fumos"), AdminFilter())
async def show_all_fumos(message: types.Message, command: CommandObject, session: AsyncSession) -> None:
    search_pattern = command.args
    if search_pattern:
        fumos = await db_search_fumos_by_name(session, search_pattern)
    else:
        fumos = await db_show_all_fumos(session)
    for fumo in fumos:
        await message.answer_photo(
            photo=fumo.file_id,
            caption=fumo.name,
            reply_markup=edit_buttons())


@router.callback_query(F.data == "delete_fumo")
async def cmd_delete_fumo_from_db(callback: types.CallbackQuery, state: FSMContext):
    fumo_name = callback.message.caption
    await state.set_state(Form.remove_fumo)
    await state.update_data(fumo_to_delete=fumo_name)
    await callback.message.answer(
        f"You are about to delete fumo {fumo_name}. Is that correct?",
        reply_markup=confirm_buttons()
    )
    await callback.answer()


@router.callback_query(Form.remove_fumo, F.data == "confirm_delete")
async def delete_fumo_from_db_confirm(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    user_data = await state.get_data()
    result = await db_delete_fumo_by_name(session, user_data['fumo_to_delete'])
    await update_fumo_ids_cache(session)
    await callback.message.answer(result)
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(Form.remove_fumo, F.data == "cancel_delete")
async def delete_fumo_from_db_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.answer()
