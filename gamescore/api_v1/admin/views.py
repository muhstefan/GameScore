from fastapi import APIRouter, Depends,status
from gamescore.api_v1.auth.dependencies import require_admin
from gamescore.api_v1.users.dependencies import prepare_user_update
from gamescore.core.db import get_db
from gamescore.core.models import User
from gamescore.core.models.games import GameCreate, Game, GameUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.api_v1.games import crud as crud_games
from gamescore.api_v1.users import crud as crud_users
from gamescore.core.models.users import UserUpdate

router = APIRouter(tags=["Admin"])

@router.get("/admin-only/")
async def admin_only_endpoint(current_admin_user = Depends(require_admin)):
    return {"message": f"Привет, {current_admin_user.username}! Это эндпоинт только для админов."}

#Секция пользователей.

@router.get("/", response_model=list[User])
async def get_users(session : AsyncSession = Depends(get_db)):
    return await crud_users.get_users(session=session)

@router.put("/{user_id}/", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud_users.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.patch("/{user_id}/", response_model=User)
async def update_user_partial(
    user_id: int,
    user_update: UserUpdate,
    update_data: dict = Depends(prepare_user_update),
    session : AsyncSession = Depends(get_db)
):
    updated_user = await crud_users.update_user(session=session, user_id=user_id, update_data=update_data)
    return updated_user

@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session : AsyncSession = Depends(get_db)
) -> None:
    await crud_users.delete_user(session=session, user_id=user_id)

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
                      current_user=Depends(require_admin)
                      ):
    return await crud_games.create_game(session=session,game_in=game_in)

@router.post("/list/", response_model=list[Game], status_code=status.HTTP_201_CREATED)
async def create_games(
    games_in: list[GameCreate],
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_admin)
):
    return await crud_games.create_games(session=session, games_in=games_in)

