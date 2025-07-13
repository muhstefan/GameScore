from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from gamescore.api_v1.rawg.client import fetch_multiple_pages
from gamescore.api_v1.rawg.service import parse_games
from gamescore.core.db import get_db
from gamescore.api_v1.games.crud import create_games
import os

router = APIRouter(tags=["RAWG"])

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
RAWG_BASE_URL = "https://api.rawg.io/api"

@router.get("/games/")
async def get_games(session: AsyncSession = Depends(get_db)):
    params = {
        "key": RAWG_API_KEY,
        "ordering": "-rating",
        "page_size": 40,
        "platforms": "4",
        "metacritic": "65,100"
    }
    try:
        raw_games = await fetch_multiple_pages(params, RAWG_BASE_URL, pages=5)
    except Exception:
        raise HTTPException(status_code=502, detail="Ошибка при запросе к RAWG API")
    games_to_create = parse_games(raw_games)
    created_games = await create_games(session=session, games_in=games_to_create)
    return {"created": len(created_games)}