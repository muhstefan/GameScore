from fastapi import Request
from gamescore.core.db import get_db
from gamescore.api_v1.auth.security import get_user_from_token

async def current_user_middleware(request: Request, call_next):
    # Выполняем логику только для путей, начинающихся с /pages
    if request.url.path.startswith("/pages"):
        request.state.current_user = None
        access_token = request.cookies.get("access_token")
        if access_token:
            token = access_token.removeprefix("Bearer ").strip()
            async with get_db() as session:
                user = await get_user_from_token(token, session)
                if user:
                    request.state.current_user = user
    else:
        request.state.current_user = None

    response = await call_next(request)
    return response