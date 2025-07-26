from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gamescore.api_v1.auth import get_user_strict
from gamescore.core.db import get_db
from gamescore.core.models.tables import Game
from . import crud
from .dependencies import game_by_id

router = APIRouter(tags=["Games"], dependencies=[Depends(get_user_strict)])


@router.get("/", response_model=list[Game])
async def get_games(session: AsyncSession = Depends(get_db)):
    return await crud.get_games(session=session)


@router.get("/{game_id}/", response_model=Game)
async def get_game(game: Game = Depends(game_by_id)):
    return game
