from fastapi import APIRouter, HTTPException,status, Depends
from microshop.core.models.game import GameUpdate,Game , GameCreate
from . import crud
from microshop.core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from . dependencies import game_by_id
from microshop.core.db import get_db

router = APIRouter(tags=["Games"])



@router.get("/",response_model=list[Game])
async def get_games(session : AsyncSession = Depends(get_db)):
    return await crud.get_games(session=session)

@router.post("/", response_model=Game,status_code=status.HTTP_201_CREATED)
async def create_game(game_in: GameCreate,
                         session : AsyncSession = Depends(get_db)):
    return await crud.create_game(session=session,game_in=game_in)

@router.get("/{game_id}/", response_model=Game)
async def get_game(game : Game = Depends(game_by_id)):
    return game


# Полное обновление объекта.
@router.put("/{game_id}/")
async def update_game(
        game_update: GameUpdate,
        game_id: int,
        session : AsyncSession = Depends(get_db)
):
    return await crud.update_game(
        session=session,
        game_id=game_id,
        game_update=game_update
    )

# Частичное обновление объекта.
@router.patch("/{game_id}/")
async def update_game_particle(
        game_update: GameUpdate,
        game_id: int,
        session : AsyncSession = Depends(get_db)
):
    return await crud.update_game(
        session=session,
        game_id=game_id,
        game_update=game_update,
        partial=True
    )

@router.delete("/{game_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
        game_id: int ,
        session : AsyncSession = Depends(get_db)
        ) -> None:
    return await crud.delete_game(session=session,game_id=game_id)

