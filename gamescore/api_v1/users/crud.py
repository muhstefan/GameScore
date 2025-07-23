from typing import cast, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд

from gamescore.core.entities.users import UserCreateDB, UserGameUpdate, UserGameFilter
from gamescore.core.models import User, Game
from sqlalchemy.engine import Result
from sqlalchemy import select, ColumnElement, delete
from gamescore.core.models.users import  UserGame, UserGameGenre, GameStatus
from gamescore.core.models.genres import Genre
from fastapi import HTTPException
from gamescore.core.db import get_one_by_fields
from sqlalchemy.orm import selectinload

async def get_users(session : AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result : Result = await session.execute(stmt)
    users = result.scalars().all()  # scalars аналог **
    return list(users)

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(
        User, user_id,
        options=[
            selectinload(User.genres),
            selectinload(User.user_games).selectinload(UserGame.game)
        ]
    )

async def get_user_game(
    session: AsyncSession,
    user_id: int,
    game_id: int
) -> UserGame | None:
    result = await session.execute(
        select(UserGame)
        .where(UserGame.user_id == user_id, UserGame.game_id == game_id)
        .options(
            selectinload(UserGame.game),
            selectinload(UserGame.user),
            selectinload(UserGame.user_game_genres).selectinload(UserGameGenre.genre),
            selectinload(UserGame.genres)
        )
    )
    return result.scalar_one_or_none()

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

async def remove_game_from_user(session: AsyncSession, user_id: int, game_id: int):

    user_game = await get_one_by_fields(session, UserGame, {"user_id": user_id, "game_id": game_id})
    if not user_game:
        raise HTTPException(status_code=404, detail="Игра не найдена у пользователя")
    await session.delete(user_game)
    await session.commit()

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
    user_game = await get_one_by_fields(
        session,
        UserGame,
        {"user_id": user_id, "game_id": game_id},
        eager_load=[selectinload(UserGame.genres)]
    )
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
    user_game = await get_user_game(session, user_id, game_id)
    if not user_game:
        raise HTTPException(status_code=404, detail="UserGame не найдена")

    update_data = user_game_update.model_dump(exclude_unset=partial)

    genre_ids = update_data.pop("genre_ids", None)
    if genre_ids is not None:
        # Удаляем старые связи
        await session.execute(
            delete(UserGameGenre).where(UserGameGenre.user_game_id == user_game.id)
        )
        # Добавляем новые связи
        new_links = [UserGameGenre(user_game_id=user_game.id, genre_id=gid) for gid in genre_ids]
        session.add_all(new_links)

        # Чтобы отразить изменения на уровне объекта
        await session.refresh(user_game)

    for field, value in update_data.items():
        setattr(user_game, field, value)

    session.add(user_game)
    await session.commit()
    await session.refresh(user_game)
    return user_game

def select_user_games_filters_query(
    user_id: int,
    filters: Optional[UserGameFilter] = None  # делаем filters опциональным
):
    query = (
        select(Game)
        .join(UserGame, Game.id == UserGame.game_id)
        .where(UserGame.user_id == user_id)
    )

    if not filters:
        # Если фильтров нет, возвращаем базовый запрос
        return query

    if filters.status:
        query = query.where(cast(ColumnElement[bool],UserGame.status == filters.status))

    if filters.min_rating:
        query = query.where(cast(ColumnElement[bool],UserGame.rating >= filters.min_rating))

    if filters.genre_ids:
        query = query.join(UserGame.genres).where(Genre.id.in_(filters.genre_ids)).distinct()

    return query

async def get_user_games_ids(session: AsyncSession, user_id: int) -> set[int]:
    user_games_query = select(UserGame).where(cast(ColumnElement[bool], UserGame.user_id == user_id))
    result = await session.execute(user_games_query)
    user_games = result.scalars().unique().all()
    return {game.game_id for game in user_games}

async def get_user_genres(session: AsyncSession, user_id: int):
    user = await get_user(session=session, user_id=user_id)
    return [{"id": genre.id, "name": genre.name} for genre in user.genres]

async def get_user_game(session: AsyncSession, user_id: int, game_id: int) -> Optional[UserGame]:
    result = await session.execute(
        select(UserGame)
        .options(
            selectinload(UserGame.game),
            selectinload(UserGame.genres),
        )
        .where(
            UserGame.user_id == user_id,
            UserGame.game_id == game_id,
        )
    )
    return result.scalar_one_or_none()