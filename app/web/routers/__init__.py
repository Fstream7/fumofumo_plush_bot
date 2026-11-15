from fastapi import APIRouter
from . import index, fumofumo


def collect_routers() -> list[APIRouter]:
    return [fumofumo.router]


router = APIRouter()
router.include_router(index.router)
router.include_router(fumofumo.router)
