from tests.fake_messages import FakeMessages
from aiogram.types import Update
from aiogram.methods import SendMessage
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods.base import TelegramType
from unittest import mock


async def test_start(bot, dp):

    bot.add_result_for(method=SendMessage, ok=True)
    result = await dp.feed_update(bot, Update(message=FakeMessages.start_command, update_id=1))
    assert result is not UNHANDLED
    outgoing_text_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_text_message, SendMessage)
    assert outgoing_text_message.text == 'Hello Test! \nSend me a post you want, I will pass it to admins'
    assert outgoing_text_message.chat_id == 42


@mock.patch("app.handlers.start.Messages")
async def test_start_with_different_message(mock_messages, bot, dp):
    mock_messages.welcome_message = "Hello, {user_full_name}!"
    bot.add_result_for(method=SendMessage, ok=True)
    result = await dp.feed_update(bot, Update(message=FakeMessages.start_command, update_id=1))
    assert result is not UNHANDLED
    outgoing_text_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_text_message, SendMessage)
    assert outgoing_text_message.text == 'Hello, Test!'
    assert outgoing_text_message.chat_id == 42
