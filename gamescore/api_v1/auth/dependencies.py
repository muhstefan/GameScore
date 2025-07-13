from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.api_v1.auth.security import get_user_from_token
from gamescore.core.db import get_db


async def get_user_for_api(
    access_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception

    token = access_token.removeprefix("Bearer ").strip()
    user = await get_user_from_token(token, session)

    if user is None:
        raise credentials_exception

    return user

async def get_user_for_website(
    access_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_db)
):
    if access_token is None:
        return None  # Нет токена — пользователь не залогинен

    token = access_token.removeprefix("Bearer ").strip()
    user = await get_user_from_token(token, session)

    return user  # Если пользователь не найден — вернётся None


def require_admin(current_user=Depends(get_user_for_api)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user