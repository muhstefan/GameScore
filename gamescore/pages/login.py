from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})