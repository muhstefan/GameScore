from fastapi import APIRouter, status, Depends
from gamescore.core.models.users import UserCreateDB, UserUpdate, User
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .dependencies import user_by_id, prepare_user_create, prepare_user_update
from gamescore.core.db import get_db

router = APIRouter(tags=["Users"])

@router.get("/", response_model=list[User])
async def get_users(session : AsyncSession = Depends(get_db)):
    return await crud.get_users(session=session)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDB = Depends(prepare_user_create),
    session : AsyncSession = Depends(get_db)
):
    user = await crud.create_user(session=session, user_data=user_data)
    return user

@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.patch("/{user_id}/", response_model=User)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session : AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_user(session=session, user_id=user_id)


@router.post("/{user_id}/games/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_game_to_user(
    user_id: int,
    game_id: int,
    session : AsyncSession = Depends(get_db)
):
    await crud.add_game_to_user(session=session, user_id=user_id, game_id=game_id)

@router.post("/users/{user_id}/genres/{genre_name}/", status_code=status.HTTP_201_CREATED)
async def create_genre_for_user(
    user_id: int,
    genre_name: str,
    session: AsyncSession = Depends(get_db)
):
    genre = await crud.create_genre_for_user(session=session, user_id=user_id, genre_name=genre_name)
    return genre