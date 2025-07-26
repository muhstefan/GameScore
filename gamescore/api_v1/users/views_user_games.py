from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from gamescore.api_v1.auth.dependencies import get_user_id
from gamescore.core.db import get_db
from gamescore.core.entities.users import UserGameUpdate, UserGameRead
from gamescore.core.models.tables import UserGame
from . import crud
from .crud import update_user_game, get_user_genres, get_user_game, delete_genre_for_user

router = APIRouter(tags=["User_Games"])


@router.post("/me/games/{game_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_game_to_current_user(
        game_id: int,
        user_id: int = Depends(get_user_id),
        session: AsyncSession = Depends(get_db)
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


@router.get("/me/genres/")
async def get_genres_for_current_user(
        user_id: int = Depends(get_user_id),
        session: AsyncSession = Depends(get_db)
):
    genres = await get_user_genres(session=session, user_id=user_id)
    return genres


@router.post("/me/games/{game_id}/genres/{genre_name}/", status_code=status.HTTP_204_NO_CONTENT)
async def add_genre_to_current_user_game(

        game_id: int,
        genre_id: int,
        user_id: int = Depends(get_user_id),
        session: AsyncSession = Depends(get_db)
):
    await crud.add_genre_to_game_for_user(session=session, user_id=user_id, game_id=game_id, genre_id=genre_id)
    return {"message": "add genre to game for user successfully."}


@router.put("/me/games/{game_id}/", response_model=UserGame)
async def update_game_for_current_user(

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


@router.delete("/me/genres/{genre_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_genre(
        genre_id: int,
        current_user: int = Depends(get_user_id),
        session: AsyncSession = Depends(get_db),
):
    # Удаляем жанр у пользователя
    try:
        await delete_genre_for_user(session=session, current_user=current_user, genre_id=genre_id)
    except HTTPException as e:
        # Пробрасываем ошибки дальше
        raise e
    return
