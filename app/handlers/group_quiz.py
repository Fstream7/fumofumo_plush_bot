import asyncio
import logging
from typing import Optional, List
from random import randint, random
from aiogram import Router, types, F, Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import input_media_animation, LinkPreviewOptions
from config import Messages, Config
from db.models import Fumo
from db.requests import db_get_random_fumo_for_quiz
from db.requests import db_quiz_add_entry, db_quiz_get_records_for_user_id
from db.requests import db_quiz_get_leaderboard
from sqlalchemy.ext.asyncio import AsyncSession
from filters.quiz import QuizFilter, QuizReplyFilter
from filters.message_from_channel import MessageFromChannelFilter
from utils.escape_for_markdown import escape_markdown
from decorators.media_group import media_group_decorator

router = Router()
router.message.filter((QuizFilter()))


class QuizForm(StatesGroup):
    quiz_fumo = State()


async def quiz_end(state: FSMContext, user_name: Optional[str]) -> None:
    """
    Clear state context and end quiz by replacing image and text.
    Ignore TelegramBadRequest error if bot cant edit post
    """
    try:
        quiz_data = await state.get_data()
        await state.clear()
        quiz_message = quiz_data.get('quiz_message')
        if quiz_message:
            if user_name:
                await quiz_message.edit_media(
                    media=input_media_animation.InputMediaAnimation(
                        type="animation",
                        media=Messages.quiz_finish_animation_id,
                        caption=Messages.quiz_finish_win_message.format(user_full_name=user_name))
                )
            else:
                await quiz_message.edit_media(
                    media=input_media_animation.InputMediaAnimation(
                        type="animation",
                        media=Messages.quiz_finish_animation_id,
                        caption=Messages.quiz_finish_fail_message
                    )
                )
    except TelegramBadRequest as error:
        logging.warning(error)


async def quiz_set_state(state: FSMContext, fumo: Fumo, quiz_message: types.Message) -> None:
    """
    Save quiz data in state context
    """
    await state.set_state(QuizForm.quiz_fumo)
    await state.update_data(fumo_name=fumo.name)
    await state.update_data(fumo_id=fumo.id)
    await state.update_data(fumo_link=fumo.source_link)
    await state.update_data(quiz_message=quiz_message)


async def quiz_start(session: AsyncSession, bot: Bot, dispatcher: Dispatcher, chat_id: int, max_delay: int = 0) -> None:
    """
    Function for scheduler to post quiz periodically.
    Random delay on max_delay time to make quiz more random
    """
    delay = randint(0, max_delay)
    logging.info("Delayed quiz_start on %d seconds", delay)
    await asyncio.sleep(delay)
    state = dispatcher.fsm.get_context(
        bot=bot, chat_id=chat_id, user_id=chat_id
    )
    fumo = await db_get_random_fumo_for_quiz(session)
    if fumo:
        await quiz_end(state, user_name=None)
        quiz_message = await bot.send_photo(
            chat_id=chat_id,
            photo=fumo.file_id,
            caption=Messages.quiz_guess_message)
        await quiz_set_state(state, fumo, quiz_message)
    await session.close()


@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    """
    Allow admin to manual start quiz in chat. End any previus quiz.
    """
    if message.from_user.id == Config.ADMIN_CHAT_ID:
        fumo = await db_get_random_fumo_for_quiz(session)
        if fumo:
            await quiz_end(state, user_name=None)
            quiz_message = await message.reply_photo(
                photo=fumo.file_id,
                caption=Messages.quiz_guess_message)
            await quiz_set_state(state, fumo, quiz_message)


@router.message(MessageFromChannelFilter())
@media_group_decorator(only_album=False)
async def random_quiz_for_channel(messages: List[types.Message], session: AsyncSession, state: FSMContext) -> None:
    """
    Randomly reply messages from linked channel with quiz
    Use media_group decorator to process albums as one message.
    """
    if random() < 0.05:
        fumo = await db_get_random_fumo_for_quiz(session)
        if fumo:
            await quiz_end(state, user_name=None)
            quiz_message = await messages[-1].reply_photo(
                photo=fumo.file_id, caption=Messages.quiz_guess_message
            )
            await quiz_set_state(state, fumo, quiz_message)


@router.message(QuizForm.quiz_fumo, F.text, QuizReplyFilter())
async def cmd_quiz_guess(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    quiz_data = await state.get_data()
    fumo_name = quiz_data['fumo_name']
    quiz_message = quiz_data['quiz_message']
    if message.reply_to_message.message_id == quiz_message.message_id:
        if message.text.lower() == fumo_name.lower() or message.text.lower() == fumo_name.split()[0].lower():
            fumo_id = quiz_data['fumo_id']
            fumo_link = quiz_data['fumo_link']
            await db_quiz_add_entry(
                session,
                user_id=message.from_user.id,
                user_name=message.from_user.full_name,
                fumo_id=fumo_id,
                group_id=message.chat.id
            )
            await message.reply(
                Messages.quiz_success_message.format(fumo=f"{fumo_name} {fumo_link if fumo_link else ''}".strip()),
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            await quiz_end(state, user_name=message.from_user.full_name)
        else:
            await message.reply(Messages.quiz_fail_message)


@router.message(Command("my_fumos"))
async def cmd_my_fumos(message: types.Message, session: AsyncSession) -> None:
    result = await db_quiz_get_records_for_user_id(session, user_id=message.from_user.id, group_id=message.chat.id)
    if len(result) > 0:
        fumo_names_text = "\n".join(
            [f"[{escape_markdown(row.fumo_name)}]({row.fumo_link}) \\- {row.fumo_count}" for row in result]
        )
        await message.reply(
            fumo_names_text,
            parse_mode=ParseMode.MARKDOWN_V2,
            link_preview_options=LinkPreviewOptions(is_disabled=True))
    else:
        await message.reply(Messages.quiz_no_fumos_in_collection_message)


@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message, session: AsyncSession) -> None:
    result = await db_quiz_get_leaderboard(session, group_id=message.chat.id)
    if len(result) > 0:
        fumo_names_text = "Top 10 users by fumo count: \n"
        fumo_names_text += "\n".join([f"{row.user_name} - {str(row.fumo_count)}" for row in result])
        await message.reply(fumo_names_text)
