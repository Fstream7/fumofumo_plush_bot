
from aiogram.filters import Command
from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import Messages, Config
from db.requests import db_get_random_fumo_for_quiz
from sqlalchemy.ext.asyncio import AsyncSession
from filters.quiz_reply import QuizReplyFilter
from filters.chat_type import ChatTypeFilter
from db.requests import db_quiz_add_entry, db_quiz_get_records_for_user_id

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


class QuizForm(StatesGroup):
    quiz_fumo = State()


@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    """
    Allow admin to manual start quiz in chat. Clean any previus quiz.
    Todo: replace this command with scheduler.
    """
    if message.from_user.id == Config.ADMIN_CHAT_ID:
        fumo = await db_get_random_fumo_for_quiz(session)
        if fumo:
            quiz_message = await message.reply_photo(
                photo=fumo.file_id,
                caption=Messages.quiz_guess_message)
            await state.clear()
            await state.set_state(QuizForm.quiz_fumo)
            await state.update_data(fumo_name=fumo.name)
            await state.update_data(quiz_message=quiz_message)
    else:
        await message.reply("You not allowed to perform this operation")


@router.message(QuizForm.quiz_fumo, F.text, QuizReplyFilter())
async def cmd_quiz_guess(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    user_data = await state.get_data()
    fumo_name = user_data['fumo_name']
    quiz_message = user_data['quiz_message']
    if message.reply_to_message.message_id == quiz_message.message_id:
        if message.text == fumo_name or message.text in fumo_name.split():
            await db_quiz_add_entry(session, user_id=message.from_user.id, fumo_name=fumo_name)
            await message.reply(Messages.quiz_success_message.format(fumo=fumo_name))
            await quiz_message.delete()
            await state.clear()
        else:
            print(message.text)
            print(fumo_name.split())
            await message.reply(Messages.quiz_fail_message)


@router.message(Command("my_fumos"))
async def cmd_fumo(message: types.Message, session: AsyncSession) -> None:
    result = await db_quiz_get_records_for_user_id(session, user_id=message.from_user.id)
    if len(result) > 0:
        fumo_names_text = "\n".join([f"{row.fumo_name} - {str(row.fumo_count)}" for row in result])
        await message.reply(fumo_names_text)
    else:
        await message.reply(Messages.quiz_no_fumos_in_collection_message)
