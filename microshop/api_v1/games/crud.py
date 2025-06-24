from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from microshop.core.models import Game
from sqlalchemy.engine import Result
from sqlalchemy import select
from .schemas import GameCreate,GameUpdate,GameUpdatePartical


async def get_games(session : AsyncSession) -> list[Game]:
    stmt = select(Game).order_by(Game.id)
    result : Result = await session.execute(stmt)
    games = result.scalars().all()  # scalars аналог **
    return list(games)

async def get_game(session: AsyncSession,game_id: int)-> Game | None:
    return await session.get(Game, game_id)

async def create_game(session: AsyncSession, game_in: GameCreate):
    game = Game(**game_in.model_dump())
    session.add(game)
    await session.commit()
    # await session.refresh(game)
    return game

async def update_game(session: AsyncSession,  #может полностью и частично обновлять объект
                         game: Game,
                         game_update: GameUpdate | GameUpdatePartical,
                         partical : bool = False
                         )->Game:
    for name, value in game_update.model_dump(exclude_unset=partical).items():
        setattr(game,name,value)
    await session.commit()
    return game

async def delete_game(session: AsyncSession,
                         game: Game,

)-> None:
    await session.delete(game)
    await session.commit()