import pytest
from utils import create_random_game, create_partial_game

@pytest.mark.asyncio
async def test_create_game(async_client):
    game_data = await create_random_game()
    response = await async_client.post("/api/v1/games/", json=game_data)
    assert response.status_code == 201
    created_game = response.json()
    assert created_game["name"] == game_data["name"]
    print("Тест 1 Создание игры - ок")

@pytest.mark.asyncio
async def test_change_game_put(async_client,create_some_games):
    game_data = await create_random_game()
    response = await async_client.put("/api/v1/games/1/", json=game_data)
    assert response.status_code == 200
    changed_game = response.json()
    assert changed_game["name"] == game_data["name"]
    print("Тест 2 PUT")


@pytest.mark.asyncio
async def test_change_game_patch(async_client,create_some_games):
    game_data = await create_partial_game()
    response = await async_client.patch("/api/v1/games/1/", json=game_data)
    assert response.status_code == 200
    changed_game = response.json()
    assert changed_game["description"] == game_data["description"] and changed_game["rating"] == game_data["rating"]
    print("Тест 3 PATCH")

@pytest.mark.asyncio
async def test_delete_game(async_client, create_some_games):
    response = await async_client.delete("/api/v1/games/1/")
    assert response.status_code == 204
    print("Тест 4 DELETE")

@pytest.mark.asyncio
async def test_get_games(async_client, create_some_games):
    response = await async_client.get("/api/v1/games/")
    games = response.json()
    assert response.status_code == 200
    print("Тест 5 GET ALL")
    print(games)



