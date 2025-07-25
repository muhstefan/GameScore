from fastapi import APIRouter, Request, Depends

from gamescore.api_v1.auth.dependencies import get_user_soft
from gamescore.templates import templates

router = APIRouter()


@router.get("/home/")
async def index_page(request: Request,
                     user=Depends(get_user_soft)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
