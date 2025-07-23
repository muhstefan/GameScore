from fastapi import APIRouter, Depends,status
from gamescore.core.db import get_db
from gamescore.core.models.games import  Game
from gamescore.core.entities.games import  GameUpdate, GameCreate
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.api_v1.games import crud as crud_games



router = APIRouter(prefix="/games", tags=["admin-games"])

#Секция игр
# Полное обновление объекта.
@router.put("/{game_id}/")
async def update_game(
        game_update: GameUpdate,
        game_id: int,
        session : AsyncSession = Depends(get_db)
):
    return await crud_games.update_game(
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
    return await crud_games.delete_game(session=session,game_id=game_id)


@router.post("/", response_model=Game,status_code=status.HTTP_201_CREATED)
async def create_game(game_in: GameCreate,
                      session : AsyncSession = Depends(get_db),
                      ):
    return await crud_games.create_game(session=session,game_in=game_in)

@router.post("/list/", response_model=list[Game], status_code=status.HTTP_201_CREATED)
async def create_games(
    games_in: list[GameCreate],
    session: AsyncSession = Depends(get_db),
):
    return await crud_games.create_games(session=session, games_in=games_in)

