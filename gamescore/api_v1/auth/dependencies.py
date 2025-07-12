from fastapi import Depends, HTTPException, status, Cookie
from jose import JWTError,jwt
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.api_v1.auth.crud import get_user_by_username
from gamescore.core.db import get_db
from gamescore.api_v1.auth.config import ALGORITHM,SECRET_KEY


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    session : AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception
    # Убираем префикс "Bearer ", если он есть
    token = access_token.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(session, username)
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user