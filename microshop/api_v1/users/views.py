from fastapi import APIRouter, status, Depends
from microshop.core.models.users import UserCreate, UserUpdate, User
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from microshop.core.db import get_db
from .dependencies import user_by_id, prepare_user_create


router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_db)):
    return await crud.get_users(session=session)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDB = Depends(prepare_user_create),
    session: AsyncSession = Depends(get_async_session)
):
    user = await create_user(session, user_data)
    return user


@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.put("/{user_id}/")
async def update_user(
        user_update: UserUpdate,
        user_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await crud.update_user(
        session=session,
        user_int=user_id,
        user_update=user_update,
        partical=False
    )


@router.patch("/{user_id}/")
async def update_user_partial(
        user_update: UserUpdate,
        user_id: int,
        session: AsyncSession = Depends(get_db)
):
    return await crud.update_user(
        session=session,
        user_int=user_id,
        user_update=user_update,
        partical=True
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_db)
) -> None:
    return await crud.delete_user(session=session, user_int=user_id)