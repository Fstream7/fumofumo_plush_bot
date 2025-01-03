from app.filters.text_is_command import TextIsCommandFilter
from tests.fake_messages import FakeMessages


async def test_text_is_command():
    filter_instance = TextIsCommandFilter()
    assert await filter_instance(FakeMessages.start_command) is True
    assert await filter_instance(FakeMessages.test_message) is False
