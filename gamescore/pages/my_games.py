from gamescore.api_v1.auth.dependencies import get_user_soft
from gamescore.api_v1.games import crud
from gamescore.core.models import db_helper
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from gamescore.templates import templates
from fastapi import Query


router = APIRouter()

@router.get("/me/games/")
async def products_page(request: Request,
                        session: AsyncSession = Depends(db_helper.session_dependency),
                        user = Depends(get_user_soft)):
    return templates.TemplateResponse("my_games.html", {"request": request, "user": user})