from fastapi.encoders import jsonable_encoder

from gamescore.api_v1.users.crud import get_user_games_ids
from gamescore.core.entities.games import GameCreate, GameUpdate
from gamescore.core.models import Game
from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from sqlalchemy.engine import Result
from sqlalchemy import select, func, Select
from sqlalchemy.orm import selectinload

GAMES_PER_PAGE = 40

async def count_query(session: AsyncSession, base_query: Select) -> int:
    count_query_ = (
        select(func.count())
        .select_from(base_query.subquery())
    )
    result = await session.execute(count_query_)
    return result.scalar_one()


async def create_games(session: AsyncSession, games_in: list[GameCreate]) -> list[Game]:

    games = [Game(**game_in.model_dump()) for game_in in games_in]
    session.add_all(games)
    await session.commit()
    return games

async def get_games(session : AsyncSession) -> list[Game]:
    stmt = select(Game).order_by(Game.id)
    result : Result = await session.execute(stmt)
    games = result.scalars().all()  # scalars аналог **
    return list(games)

def select_games_pagination():
    return select(Game).order_by(Game.name)

async def get_games_pagination(session: AsyncSession,
                               query: Select,
                               page: int,
                               user_id: int | None = None) -> [list[Game], int]:

    total_games = await count_query(session,query)
    total_pages = (total_games + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE
    offset = (page - 1) * GAMES_PER_PAGE
    query = query.limit(GAMES_PER_PAGE).offset(offset)

    result = await session.execute(query)
    games = result.scalars().all()
    games_dicts = jsonable_encoder(games)
    user_game_ids = set()
    if user_id:
        # Получаем ID игр, которые пользователь добавил
        user_game_ids = await get_user_games_ids(session, user_id)

    # Помечаем каждую игру, есть ли она у пользователя
    for game in games_dicts:
        game['in_library'] = game['id'] in user_game_ids

    return games_dicts, total_pages

async def get_game(session: AsyncSession,game_id: int)-> Game | None:
    return await session.get(Game, game_id)


async def create_game(session: AsyncSession, game_in: GameCreate):
    game = Game(**game_in.model_dump())
    session.add(game)
    await session.commit()
    return game

async def update_game(session: AsyncSession,  # может полностью и частично обновлять объект
                         game_id: int,  # объект игры, которую нужно обновить
                         game_update: GameUpdate, # данные обновления игры
                         partial : bool = False
                         )->Game:
    game = await get_game(session, game_id)
    for name_field, value in game_update.model_dump(exclude_unset=partial).items(): # метод Pydantic-модели, который возвращает словарь с данными из game_update.
        setattr(game,name_field,value)
    await session.commit()
    return game

async def delete_game(session: AsyncSession,
                         game_id: int,

)-> None:
    game = await get_game(session, game_id)
    await session.delete(game)
    await session.commit()