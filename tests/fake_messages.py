import datetime
from aiogram.types import Chat, Message, User
from dataclasses import dataclass


@dataclass
class FakeMessages():
    private_chat = Chat(id=42, type="private")
    test_user = User(id=42, is_bot=False, first_name="Test", username="test")

    start_command = Message(
        message_id=42,
        date=datetime.datetime.now(),
        text="/start",
        chat=private_chat,
        from_user=test_user,
    )
    test_message = Message(
        message_id=42,
        date=datetime.datetime.now(),
        text="test",
        chat=private_chat,
        from_user=test_user,
    )
