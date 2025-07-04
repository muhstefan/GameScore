from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from microshop.core.models import db_helper, Game
from . import crud


# Path (берем ее из пути URL)
async def game_by_id(game_id: Annotated[int,Path],
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency))\
        -> Game:
        game = await crud.get_game(session=session, game_id=game_id)
        if game:
            return game
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {game_id} NOT FOUND(")