from gamescore.core.models import User
from gamescore.api_v1.users.dependencies import prepare_user_update
from gamescore.core.models.users import UserUpdate
from gamescore.api_v1.users import crud as crud_users
from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.db import get_db


router = APIRouter(prefix="/users", tags=["admin-users"])

#Секция пользователей.

@router.get("/", response_model=list[User])
async def get_users(session : AsyncSession = Depends(get_db)):
    return await crud_users.get_users(session=session)

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud_users.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.patch("/{user_id}/", response_model=User)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud_users.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session : AsyncSession = Depends(get_db)
) -> None:
    await crud_users.delete_user(session=session, user_id=user_id)
