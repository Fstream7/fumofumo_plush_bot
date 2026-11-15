from fastapi import APIRouter
from . import fumofumo


def collect_routers() -> list[APIRouter]:
    return [fumofumo.router]


router = APIRouter()
router.include_router(fumofumo.router)
