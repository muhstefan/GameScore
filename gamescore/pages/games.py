from typing import Annotated
from sqlalchemy import Select
from gamescore.api_v1.auth.dependencies import get_user_soft, get_user_id
from gamescore.api_v1.games.crud import get_games_pagination, select_games_pagination
from gamescore.api_v1.users.crud import select_user_games_filters_query
from gamescore.core.models import db_helper
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.entities.users import  UserGameFilter
from gamescore.templates import templates
from fastapi import Query
from sqlalchemy.orm import selectinload

router = APIRouter()
GAMES_PER_PAGE = 40


@router.get("/games/")
async def products_page(request: Request,
                        user = Depends(get_user_soft)):
    return templates.TemplateResponse("games.html", {"request": request, "user": user})

@router.get("/games/list/")
async def games_list_container(
    request: Request,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user_id: int | None = Depends(get_user_id),
    query: Select = Depends(select_games_pagination),
):
    games, total_pages = await get_games_pagination(session, page=page, user_id=user_id, query=query)

    return templates.TemplateResponse(
        "games_list_container.html",
        {
            "request": request,
            "games": games,
            "page": page,
            "total_pages": total_pages,
        }
    )

@router.get("/me/games/list/")
async def read_user_games(
    filters: Annotated[UserGameFilter, Depends()],
    request: Request,
    user_id: int | None = Depends(get_user_id),
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = select_user_games_filters_query(filters=filters,user_id=user_id)
    games, total_pages = await get_games_pagination(session, page=page, user_id=user_id, query=query)

    # Возвращаем шаблон с дополнительным флагом для кнопок
    return templates.TemplateResponse(
        "my_games_list_container.html",
        {
            "request": request,
            "games": games,
            "page": page,
            "total_pages": total_pages,
        }
    )