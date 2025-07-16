from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from gamescore.api_v1.auth.config import Production
from gamescore.api_v1.auth.dependencies import get_user_soft
from gamescore.templates import templates
from fastapi import Response
from fastapi import APIRouter, Request, Depends

router = APIRouter()

@router.get("/login/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/logout/")
async def logout(user = Depends(get_user_soft)):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=Production
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=Production
    )
    return response