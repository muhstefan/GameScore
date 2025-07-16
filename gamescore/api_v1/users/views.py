from fastapi import APIRouter, status, Depends
from gamescore.core.models.users import UserCreateDB, UserUpdate, User, UserPublic, UserGameUpdate, UserGame
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .crud import update_user_game
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


@router.post("/me/games/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_game_to_current_user(
    user_id: int,
    game_id: int,
    session : AsyncSession = Depends(get_db)
):
    await crud.add_game_to_user(session=session, user_id=user_id, game_id=game_id)

    return {"message": "Game added to user successfully."}

@router.post("me/genres/{genre_name}/", status_code=status.HTTP_201_CREATED)
async def create_genre_for_current_user(
    user_id: int,
    genre_name: str,
    session: AsyncSession = Depends(get_db)
):
    genre = await crud.create_genre_for_user(session=session, user_id=user_id, genre_name=genre_name)
    return {"message": "create genre for user successfully."}

@router.post("/me/games/{game_id}/genres/{genre_name}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_genre_to_user_game(
    user_id: int,
    game_id: int,
    genre_id: int,
    session: AsyncSession = Depends(get_db)
):
    await crud.add_genre_to_game_for_user(session=session, user_id=user_id, game_id=game_id, genre_id=genre_id)
    return {"message": "add genre to game for user successfully."}


@router.put("/users/{user_id}/games/{game_id}/", response_model=UserGame)
async def update_user_game_view(
    user_id: int,
    game_id: int,
    user_game_update: UserGameUpdate,
    session: AsyncSession = Depends(get_db),
):
    """
    Частичное обновление записи UserGame (статус, рейтинг).
    """
    updated_user_game = await update_user_game(
        session=session,
        user_id=user_id,
        game_id=game_id,
        user_game_update=user_game_update,
        partial=True,
    )
    return updated_user_game