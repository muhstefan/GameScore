from typing import cast

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from gamescore.core.models import User
from sqlalchemy.engine import Result
from sqlalchemy import select, ColumnElement
from gamescore.core.models.users import UserCreateDB, UserGame, UserGameGenre, GameStatus, UserGameUpdate, \
    UserGameFilter
from gamescore.core.models.genres import Genre
from fastapi import HTTPException
from gamescore.core.db import get_one_by_fields
from sqlalchemy.orm import selectinload

async def get_users(session : AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result : Result = await session.execute(stmt)
    users = result.scalars().all()  # scalars аналог **
    return list(users)

async def get_user(session: AsyncSession,user_id: int)-> User | None:
    return await session.get(User, user_id)

async def create_user(session: AsyncSession, user_data: UserCreateDB):
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user

async def update_user(
        session: AsyncSession,
        user_id: int,
        update_data: dict
) -> User:
    user = await get_user(session, user_id)
    for name, value in update_data.items():
        setattr(user, name, value)
    await session.commit()
    return user

async def delete_user(session: AsyncSession,
                      user_id: int
                      ) -> None:
    user = await get_user(session, user_id)
    await session.delete(user)
    await session.commit()


async def add_game_to_user(session: AsyncSession,
                           user_id: int,
                           game_id: int):
    user_game = UserGame(user_id=user_id, game_id=game_id, status=GameStatus.wait)
    session.add(user_game)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409, detail="Игра уже добавлена к пользователю"
        )

async def create_genre_for_user(session: AsyncSession,
                                user_id: int,
                                genre_name: str) -> Genre:
    genre = Genre(name=genre_name, user_id=user_id)
    session.add(genre)
    try:
        await session.commit()
        await session.refresh(genre)
        return genre
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Жанр с таким именем уже существует")

async def add_genre_to_game_for_user(
    session: AsyncSession,
    user_id: int,
    game_id: int,
    genre_id: int
):
    # 1. Найти UserGame
    user_game = await get_one_by_fields(session, UserGame, {"user_id": user_id, "game_id": game_id})
    if not user_game:
        raise HTTPException(status_code=404, detail="Игры пользователя не найдены")

    # 2. Найти Genre по id и user_id для безопасности, чтобы жанр принадлежал именно этому пользователю
    genre = await get_one_by_fields(session, Genre, {"user_id": user_id, "id": genre_id})
    if not genre:
        raise HTTPException(status_code=404, detail=f"Жанр с id '{genre_id}' не найден для текущего пользователя.")

    # 3. Создаём связь
    user_game_genre = UserGameGenre(user_game_id=user_game.id, genre_id=genre.id)
    session.add(user_game_genre)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Жанр уже добавлен к игре пользователя")


async def update_user_game(
        session: AsyncSession,
        user_id: int,
        game_id: int,
        user_game_update: UserGameUpdate,
        partial: bool = True,
) -> UserGame:
    # 1. Найти объект UserGame по ключам
    user_game = await get_one_by_fields(session, UserGame, {"user_id": user_id, "game_id": game_id})
    if not user_game:
        raise HTTPException(status_code=404, detail="Запись UserGame не найдена")

    # 2. Получить словарь обновления из Pydantic-модели
    update_data = user_game_update.model_dump(exclude_unset=partial)  # Для Pydantic v2

    # 3. Обновить поля у модели SQLAlchemy
    for field, value in update_data.items():
        setattr(user_game, field, value)

    # 4. Сохранить изменения
    session.add(user_game)
    await session.commit()
    await session.refresh(user_game)
    return user_game


async def get_user_games(
    session: AsyncSession,
    user_id: int,
    filters: UserGameFilter
) -> list[UserGame]:
    query = select(UserGame).where(cast(ColumnElement[bool], UserGame.user_id == user_id))

    if filters.status:
        query = query.where(cast(ColumnElement[bool],UserGame.status == filters.status))

    if filters.min_rating:
        query = query.where(cast(ColumnElement[bool],UserGame.rating >= filters.min_rating))

    if filters.genre_ids:
        query = query.join(UserGame.genres).where(Genre.id.in_(filters.genre_ids)).distinct()

    result = await session.execute(query)
    user_games = result.scalars().unique().all()
    return user_games