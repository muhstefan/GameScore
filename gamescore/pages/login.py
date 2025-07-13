from fastapi import APIRouter, Request
from gamescore.templates import templates

router = APIRouter()

@router.get("/login/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})