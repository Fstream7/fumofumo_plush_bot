import pytest
from aiogram import Dispatcher
from tests.mocked_bot import MockedBot
from app.handlers import start


@pytest.fixture()
def bot() -> MockedBot:
    return MockedBot()


@pytest.fixture(scope="session")
def dp() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    return dispatcher
