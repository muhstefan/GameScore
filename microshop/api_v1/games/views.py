from fastapi import APIRouter, HTTPException,status, Depends
from microshop.api_v1.games.schemas import GameUpdate, GameUpdatePartical
from requests import session

from . import crud
from .schemas import Game , GameCreate
from microshop.core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from . dependencies import game_by_id

router = APIRouter(tags=["Games"])



@router.get("/",response_model=list[Game])
async def get_games(session : AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_games(session=session)

@router.post("/", response_model=Game,status_code=status.HTTP_201_CREATED)
async def create_game(game_in: GameCreate,
                         session : AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_game(session=session,game_in=game_in)

@router.get("/{game_id}/", response_model=Game)
async def get_game(game : Game = Depends(game_by_id)):
    return game

@router.put("/{game_id}/")
async def update_game(
        game_update: GameUpdate,
        game : Game = Depends(game_by_id),
        session : AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update
    )


@router.patch("/{game_id}/")
async def update_game_particle(
        game_update: GameUpdatePartical,
        game : Game = Depends(game_by_id),
        session : AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_game(
        session=session,
        game=game,
        game_update=game_update,
        partical=True
    )

@router.delete("/{game_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
        session : AsyncSession = Depends(db_helper.scoped_session_dependency),
        game : Game = Depends(game_by_id)) -> None:
    return await crud.delete_game(session=session,game=game)

