from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.db import get_db
from gamescore.api_v1.games.crud import create_games
import httpx
import os
from gamescore.core.models.games import GameCreate

router = APIRouter(tags=["RAWG"])

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
RAWG_BASE_URL = "https://api.rawg.io/api"

@router.get("/games/")
async def get_games(session: AsyncSession = Depends(get_db)):

    params = {
        "key": RAWG_API_KEY,
        "ordering": "-rating",
        "page_size": 250,
        "platforms": "4"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RAWG_BASE_URL}/games", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Ошибка при запросе к RAWG API")
        raw_data = response.json()

        games_to_create = []
        for raw_game in raw_data.get("results", []):
            # Берём только name и image (image — обычно в поле background_image)
            name = raw_game.get("name")
            image = raw_game.get("background_image")

            if not name:
                continue  # пропускаем, если нет имени

            game_in = GameCreate(
                name=name,
                image=image
            )
            games_to_create.append(game_in)

        created_games = await create_games(session=session, games_in=games_to_create)

        return {"created": len(created_games)}
