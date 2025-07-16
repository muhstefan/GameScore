from gamescore.api_v1.auth.dependencies import get_user_soft
from gamescore.api_v1.games import crud
from gamescore.core.models import db_helper
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from gamescore.templates import templates
from fastapi import Query


router = APIRouter()

@router.get("/games/")
async def products_page(request: Request,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                        user = Depends(get_user_soft)):
    return templates.TemplateResponse("games.html", {"request": request, "user": user})

@router.get("/games/list/")
async def games_list_container(
    request: Request,
    page: int = Query(1, ge=1),  # параметр page с дефолтом 1 и минимум 1
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    GAMES_PER_PAGE = 40

    # Считаем общее количество игр
    total_games = await crud.count_games(session)
    total_pages = (total_games + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE

    offset = (page - 1) * GAMES_PER_PAGE

    # Получаем игры для текущей страницы
    games = await crud.get_games_pagination(session, limit=GAMES_PER_PAGE, offset=offset)
    games_dicts = jsonable_encoder(games)

    # Возвращаем только часть шаблона с играми и пагинацией
    return templates.TemplateResponse(
        "games_list_container.html",
        {
            "request": request,
            "games": games_dicts,
            "page": page,
            "total_pages": total_pages,
        }
    )

