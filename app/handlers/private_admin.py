from aiogram import Router, F, types
from aiogram.types import Message
from filters.admin import AdminFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

router = Router()


class Form(StatesGroup):
    name = State()


@router.message(Command("get_stickers_id"), AdminFilter())
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Send me a stickers, I will write their file_id. \nSend /cancel to stop")


@router.message(Form.name, F.sticker)
async def message_with_sticker(message: Message):
    await message.answer(f"Sticker file_id {message.sticker.file_id}")


@router.message(Form.name, Command("cancel"))
@router.message(Form.name, F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancelled.")
