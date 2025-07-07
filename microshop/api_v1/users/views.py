from fastapi import APIRouter, status, Depends
from microshop.core.models.users import UserCreateDB, UserUpdate, User
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .dependencies import user_by_id, prepare_user_create, prepare_user_update
from microshop.core.models import db_helper

router = APIRouter(tags=["Users"])

@router.get("/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_users(session=session)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDB = Depends(prepare_user_create),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await crud.create_user(session, user_data)
    return user

@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    updated_user = await crud.update_user(session, user_id, update_data)
    return updated_user

@router.patch("/{user_id}/", response_model=User)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    updated_user = await crud.update_user(session, user_id, update_data)
    return updated_user

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    await crud.delete_user(session, user_id)
