from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gamescore.api_v1.auth.dependencies import get_user_soft
from gamescore.core.models import db_helper
from gamescore.templates import templates

router = APIRouter()


@router.get("/me/games/")
async def products_page(request: Request,
                        session: AsyncSession = Depends(db_helper.session_dependency),
                        user=Depends(get_user_soft)):
    return templates.TemplateResponse("my_games.html", {"request": request, "user": user})
