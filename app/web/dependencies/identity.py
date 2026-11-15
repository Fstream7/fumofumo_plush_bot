import uuid
from fastapi import Request, Response

COOKIE_NAME = "user_uuid"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365


async def get_user_uuid(
    request: Request,
    response: Response,
) -> str:
    user_uuid = request.cookies.get(COOKIE_NAME)
    if not user_uuid:
        user_uuid = str(uuid.uuid4())
        response.set_cookie(
            key=COOKIE_NAME,
            value=user_uuid,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
        )
    return user_uuid
