from gamescore.core.models import Game
from gamescore.core.models.games import GameCreate,GameUpdate
from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from sqlalchemy.engine import Result
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

async def count_games(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Game))
    total = result.scalar_one()
    return total


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

async def get_games_pagination(session: AsyncSession, limit: int, offset: int) -> list[Game]:
    query = select(Game).order_by(Game.name).limit(limit).offset(offset)
    result = await session.execute(query)
    return list(result.scalars().all())

async def get_game(session: AsyncSession,game_id: int)-> Game | None:
    return await session.get(Game, game_id)


async def create_game(session: AsyncSession, game_in: GameCreate):
    game = Game(**game_in.model_dump())
    session.add(game)
    await session.commit()
    # await session.refresh(game)
    return game

async def update_game(session: AsyncSession,  #может полностью и частично обновлять объект
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