from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import Config

router = Router()


class Form(StatesGroup):
    name = State()


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Command("propose"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("Send me a post you want, I will pass it to Admins")


@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    for chat_id in Config.ADMIN_LISTS:
        await message.forward(chat_id)
    await message.answer("Thanks, message sent to admins, you are greatly appreciated!")
    await message.answer_sticker(sticker=Config.THANKS_STIKER)
