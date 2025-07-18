from fastapi import APIRouter, status, Depends
from gamescore.core.models.users import UserCreateDB, UserUpdate, User, UserPublic, UserGameUpdate, UserGame
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .views_user_games import router as user_games_router
from .dependencies import prepare_user_create, prepare_user_update
from gamescore.core.db import get_db
from gamescore.api_v1.auth import get_user_strict

router = APIRouter(tags=["Users"])

# Создавать пользователей может даже не вошедший в систему пользователь (защита от DDOS?)
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDB = Depends(prepare_user_create),
    session : AsyncSession = Depends(get_db)
):
    user = await crud.create_user(session=session, user_data=user_data)
    return user


@router.get("/{user_id}/", response_model=UserPublic)
async def get_user(
                user_id: int,
                current_user: User = Depends(get_user_strict), # Проверка, что пользователь login in
                session: AsyncSession = Depends(get_db)
            ):
    user = await crud.get_user(session, user_id)
    return user

@router.put("/me/", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db),
    current_user: User = Depends(get_user_strict)
):
    user_id = current_user.id
    updated_user = await crud.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    user_id: int,
    session : AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_user(session=session, user_id=user_id)

