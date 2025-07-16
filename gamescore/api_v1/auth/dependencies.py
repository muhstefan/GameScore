from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.db import get_db
from gamescore.api_v1.users.crud import get_user


async def get_user_strict(
    request: Request, # Добавляем Request как параметр
    session: AsyncSession = Depends(get_db)
):
    # Вызываем get_user_for_website, передавая ей request и session
    user = await get_user_soft(request, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_user_soft(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        return None  # Гость или неавторизованный пользователь

    user = await get_user(session, int(user_id))
    return user

def require_admin(current_user=Depends(get_user_strict)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user