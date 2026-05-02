import asyncio
import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    input_media_animation,
    ReplyKeyboardRemove,
    CallbackQuery,
)
from filters.chat_type import ChatTypeFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from random import shuffle
from db.requests import (
    db_get_quiz_fumo_ids,
    db_get_quiz_fumo_by_id,
    db_get_random_quiz_names,
    db_update_leaderboard,
    db_quiz_get_globabl_leaderboard,
)
from config import Messages
from keyboards.quiz_buttons import quiz_buttons, stop_button, continue_button

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["private"]))


class Form(StatesGroup):
    quiz_is_active = State()


async def quiz_clean_post(
    bot: Bot, current_fumo_link: str, quiz_chat_id: str, quiz_message_id: str
) -> None:
    try:
        await bot.edit_message_media(
            media=input_media_animation.InputMediaAnimation(
                type="animation",
                media=Messages.quiz_finish_animation_id,
                caption=current_fumo_link,
            ),
            chat_id=quiz_chat_id,
            message_id=quiz_message_id,
        )
    except TelegramBadRequest as error:
        logging.error(error)


async def quiz_end(state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    """
    End quiz, show user score and clear state
    """
    quiz_data = await state.get_data()
    quiz_score = quiz_data["quiz_score"]
    quiz_chat_id = quiz_data["quiz_chat_id"]
    quiz_message_id = quiz_data["quiz_message_id"]
    current_fumo_link = quiz_data["current_fumo_link"]
    quiz_username = quiz_data["quiz_username"]
    quiz_user_id = quiz_data["quiz_user_id"]
    await quiz_clean_post(bot, current_fumo_link, quiz_chat_id, quiz_message_id)
    await state.clear()
    if quiz_score > 0:
        await db_update_leaderboard(session, quiz_username, quiz_user_id, quiz_score)
    await bot.send_message(
        chat_id=quiz_chat_id,
        text=Messages.quiz_finish_message.format(score=str(quiz_score)),
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.quiz_is_active, Command("stop"))
@router.message(Form.quiz_is_active, F.text.casefold() == "stop")
@router.callback_query(Form.quiz_is_active, F.data == "stop")
async def stop_handler(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
) -> None:
    """
    Allow user to stop game
    """
    await quiz_end(state, session, bot)


@router.message(Form.quiz_is_active, F.text.casefold() == "continue")
@router.callback_query(Form.quiz_is_active, F.data == "continue")
async def quiz_continue(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
) -> None:
    """
    Continue game after long response, to awoid flood when user not active
    """
    await message.reply("Continuing", reply_markup=stop_button())
    await iterate_quiz(state, session, bot)


@router.message(Command("quiz"))
async def private_quiz_start(
    message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot
) -> None:
    """
    Init quiz
    """
    await state.set_state(Form.quiz_is_active)
    fumo_id_list = await db_get_quiz_fumo_ids(session)
    shuffle(fumo_id_list)
    await state.update_data(fumo_id_list=fumo_id_list)
    await state.update_data(curent_position=0)
    await state.update_data(quiz_chat_id=message.chat.id)
    await state.update_data(quiz_score=0)
    await state.update_data(quiz_username=message.from_user.full_name)
    await state.update_data(quiz_user_id=message.from_user.id)
    await message.answer(
        "Guess a plushies characters name game.\n"
        "You will have only 10 second to choose correct answer\n"
        "Send /stop to stop game",
        reply_markup=stop_button(),
    )
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2)
    await private_quiz_post(state, session, bot)


async def private_quiz_post(state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    """
    Post quiz fumo
    Get fumo from db with current position and add it to list with 3 more names
    """
    quiz_data = await state.get_data()
    fumo_id_list = quiz_data["fumo_id_list"]
    curent_position = quiz_data["curent_position"]
    quiz_chat_id = quiz_data["quiz_chat_id"]
    fumo = await db_get_quiz_fumo_by_id(session, fumo_id_list[curent_position])
    if fumo:
        await state.update_data(current_fumo_name=fumo.name)
        await state.update_data(current_fumo_link=fumo.source_link)
        fumo_names = await db_get_random_quiz_names(session, correct_name=fumo.name)
        fumo_names.append(fumo.name)
        shuffle(fumo_names)
        quiz_message = await bot.send_photo(
            chat_id=quiz_chat_id,
            photo=fumo.file_id,
            reply_markup=quiz_buttons(fumos_list=fumo_names),
        )
        await state.update_data(quiz_message_id=quiz_message.message_id)
        await asyncio.sleep(10)
        current_state = await state.get_state()
        if current_state == Form.quiz_is_active:
            current_data = await state.get_data()
            new_fumo_name = current_data.get("current_fumo_name")
            if new_fumo_name == fumo.name:
                await quiz_message.reply(
                    Messages.quiz_timeout_message, reply_markup=continue_button()
                )
    else:
        await bot.send_message(
            chat_id=quiz_chat_id, text=Messages.fumofumo_message_not_found
        )


async def iterate_quiz(state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    """
    Iterate next fumo for quiz
    Edit previus message to avoid cheating
    If last fumo, clear state and send score
    """
    quiz_data = await state.get_data()
    quiz_chat_id = quiz_data["quiz_chat_id"]
    quiz_message_id = quiz_data["quiz_message_id"]
    current_fumo_link = quiz_data["current_fumo_link"]
    await quiz_clean_post(bot, current_fumo_link, quiz_chat_id, quiz_message_id)
    curent_position = quiz_data["curent_position"]
    fumo_id_list = quiz_data["fumo_id_list"]
    if curent_position < (len(fumo_id_list) - 1):
        curent_position += 1
        await state.update_data(curent_position=curent_position)
        await bot.send_chat_action(chat_id=quiz_chat_id, action="typing")
        await asyncio.sleep(0.5)
        await private_quiz_post(state, session, bot)
    else:
        await quiz_end(state, session, bot)


@router.callback_query(Form.quiz_is_active)
async def process_quiz_answers(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext, bot: Bot
):
    """
    Process quiz answers, triger next quiz
    """
    quiz_data = await state.get_data()
    current_fumo_name = quiz_data.get("current_fumo_name")
    await state.update_data(current_fumo_name=None)
    quiz_score = quiz_data["quiz_score"]
    if callback.data == current_fumo_name:
        await callback.message.reply(Messages.quiz_pass_message)
        quiz_score += 1
        await state.update_data(quiz_score=quiz_score)
    else:
        await callback.message.reply(Messages.quiz_fail_message)
    await callback.answer()
    await iterate_quiz(state, session, bot)


@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message, session: AsyncSession) -> None:
    result = await db_quiz_get_globabl_leaderboard(session)
    if len(result) > 0:
        fumo_names_text = "Users by record: \n"
        fumo_names_text += "\n".join(
            [f"{row.user_name} - {str(row.record)}" for row in result]
        )
        await message.reply(fumo_names_text)
