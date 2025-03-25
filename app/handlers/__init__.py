from aiogram import Router
from . import get_id
from . import fumofumo
from . import quiz
from . import group_members
from . import group_delete_messages_with_blacklist
from . import privacy
from . import start
from . import private_admin
from . import private_users


def collect_routers() -> list[Router]:
    return [
        start.router,
        privacy.router,
        fumofumo.router,
        quiz.router,
        get_id.router,
        private_admin.router,
        private_users.router,
        group_members.router,
        group_delete_messages_with_blacklist.router,
    ]
