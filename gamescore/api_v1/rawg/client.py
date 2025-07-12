import httpx

async def fetch_games_from_rawg(params: dict, base_url: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/games", params=params)
        response.raise_for_status()
        return response.json().get("results", [])