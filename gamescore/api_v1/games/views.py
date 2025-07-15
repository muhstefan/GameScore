from fastapi import APIRouter, HTTPException,status, Depends
from gamescore.core.models.games import GameUpdate,Game , GameCreate
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from . dependencies import game_by_id
from gamescore.core.db import get_db
from gamescore.api_v1.auth import get_user_for_api, require_admin

router = APIRouter(tags=["Games"])


@router.get("/",response_model=list[Game])
async def get_games(session : AsyncSession = Depends(get_db),
                    current_user=Depends(get_user_for_api)):
    return await crud.get_games(session=session)


@router.get("/{game_id}/", response_model=Game)
async def get_game(game : Game = Depends(game_by_id),
                   current_user=Depends(get_user_for_api)):
    return game


