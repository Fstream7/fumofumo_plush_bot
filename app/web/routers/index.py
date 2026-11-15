from fastapi import APIRouter
from fastapi import Request
from web.templates import templates

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
