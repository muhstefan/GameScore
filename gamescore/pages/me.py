from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from gamescore.api_v1.auth.dependencies import get_user_for_website
from gamescore.templates import templates

router = APIRouter()

@router.get("/me/")
async def me_page(request: Request,
                  user = Depends(get_user_for_website)):
    if user is None:
        return RedirectResponse(url="/pages/login/", status_code=302)
    return templates.TemplateResponse("me.html", {"request": request, "user": user})