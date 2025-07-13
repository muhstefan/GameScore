import asyncio
import httpx

async def fetch_games_from_rawg(params: dict, base_url: str, page: int) -> list[dict]:
    params_with_page = params.copy()
    params_with_page["page"] = page
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/games", params=params_with_page)
        response.raise_for_status()
        return response.json().get("results", [])

async def fetch_multiple_pages(params: dict, base_url: str, pages: int = 5) -> list[dict]:
    tasks = [
        fetch_games_from_rawg(params, base_url, page)
        for page in range(1, pages + 1)
    ]
    results = await asyncio.gather(*tasks)
    games = [game for page_games in results for game in page_games]
    return games