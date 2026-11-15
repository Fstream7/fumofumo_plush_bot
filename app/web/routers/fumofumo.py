from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from web.dependencies.identity import get_user_uuid
from web.dependencies.db_session import get_db_session
from web.templates import templates
from db.requests import db_get_fumo_by_id
from config import Config, Messages

router = APIRouter(prefix="/fumofumo")


@router.get("", response_class=HTMLResponse)
async def fumofumo(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
    user_uuid: str = Depends(get_user_uuid),
) -> HTMLResponse:
    """
    Return fumofumo of the day
    """
    converted_date = datetime.now(ZoneInfo(Config.TIMEZONE))
    fumo_string = f"{user_uuid}_{converted_date.strftime('%Y%m%d')}"
    fumo_hash = hashlib.blake2b(
        fumo_string.encode(),
        digest_size=8,
        salt=str.encode(Config.HASH_SALT.get_secret_value()),
    ).hexdigest()
    fumo_id = int(fumo_hash, 16)

    fumo = await db_get_fumo_by_id(session, fumo_id)
    if fumo:
        context = {
            "name": fumo.name,
            "image": f"{fumo.name}.jpg",
            "link": fumo.source_link,
        }
    else:
        context = {"name": Messages.fumofumo_message_not_found, "image": ""}
    template_response = templates.TemplateResponse(
        request=request,
        name="fumofumo.html",
        context=context,
    )
    template_response.headers.raw.extend(response.headers.raw)
    return template_response
