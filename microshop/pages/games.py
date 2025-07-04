from microshop.api_v1.games import crud
from microshop.core.models import db_helper
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from microshop.templates import templates

router = APIRouter()

@router.get("/games")
async def products_page(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    games = await crud.get_games(session)
    games_dicts = jsonable_encoder(games)  # Преобразуем модели в JSON-совместимые словари
    return templates.TemplateResponse("games.html", {"request": request, "games": games_dicts})