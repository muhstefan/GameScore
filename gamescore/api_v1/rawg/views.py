from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.db import get_db
import httpx
import os


router = APIRouter(tags=["RAWG"])

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
RAWG_BASE_URL = "https://api.rawg.io/api"

@router.get("/games/")
async def get_games(session: AsyncSession = Depends(get_db)):

    params = {
        "key": RAWG_API_KEY,
        "ordering": "-rating",
        "page_size": 250
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RAWG_BASE_URL}/games", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Ошибка при запросе к RAWG API")
        data = response.json()

    return data