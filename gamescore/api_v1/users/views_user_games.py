from typing import Annotated
from fastapi import APIRouter, status, Depends, Query, HTTPException
from gamescore.core.models.users import UserGameUpdate, UserGame, UserGameFilter
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .crud import update_user_game, select_user_games_filters_query, get_user_genres_names, get_user_game

from gamescore.core.db import get_db
from ..auth.dependencies import get_user_id
from ...core.models.games import UserGameRead

router = APIRouter(tags=["User_Games"])

@router.post("/me/games/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_game_to_current_user(
    game_id: int,
    user_id: int = Depends(get_user_id),
    session : AsyncSession = Depends(get_db)
):
    await crud.add_game_to_user(session=session, user_id=user_id, game_id=game_id)

    return {"message": "Game added to user successfully."}

@router.delete("/me/games/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_game_from_current_user(
    game_id: int,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_db)
):
    await crud.remove_game_from_user(session=session, user_id=user_id, game_id=game_id)
    return

@router.post("/me/genres/{genre_name}/", status_code=status.HTTP_201_CREATED)
async def create_genre_for_current_user(
    genre_name: str,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_db)
):
    genre = await crud.create_genre_for_user(session=session, user_id=user_id, genre_name=genre_name)
    return {"message": "create genre for user successfully."}

@router.get("/me/genres/names/", response_model=list[str])
async def get_genres_names_for_current_user(
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_db)
):
    names = await get_user_genres_names(session=session, user_id=user_id)
    return list(names)


@router.post("/me/games/{game_id}/genres/{genre_name}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_genre_to_current_user_game(

    game_id: int,
    genre_id: int,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_db)
):
    await crud.add_genre_to_game_for_user(session=session, user_id=user_id, game_id=game_id, genre_id=genre_id)
    return {"message": "add genre to game for user successfully."}


@router.put("/me/{user_id}/games/{game_id}/", response_model=UserGame)
async def update_current_user_game_view(

    game_id: int,
    user_game_update: UserGameUpdate,
    user_id: int = Depends(get_user_id),
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

@router.get("/me/games/{game_id}/", response_model=UserGameRead)
async def get_current_user_game_view(
    game_id: int,
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(get_db)
):
    user_game = await get_user_game(session, user_id, game_id)
    if user_game is None:
        raise HTTPException(status_code=404, detail="Игра пользователя не найдена")
    return user_game