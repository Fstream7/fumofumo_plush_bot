from aiogram import Router
from . import get_id
from . import fumofumo
from . import chat_members
from . import privacy
from . import start
from . import private_admin
from . import private_users


def collect_routers() -> list[Router]:
    return [
        start.router,
        privacy.router,
        fumofumo.router,
        get_id.router,
        private_admin.router,
        private_users.router,
        chat_members.router,
    ]
