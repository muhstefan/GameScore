import pytest
from utils import create_random_game, create_partial_game


@pytest.mark.asyncio
async def test_create_game(login_admin_session):
    game_data = await create_random_game()
    response = await login_admin_session.post("/api/v1/admin/games/", json=game_data)
    assert response.status_code == 201
    created_game = response.json()
    assert created_game["name"] == game_data["name"]
    print("Тест 1 Создание игры - ок")

@pytest.mark.asyncio
async def test_change_game_put(create_some_games, login_admin_session):
    game_data = await create_random_game()
    response = await login_admin_session.put("/api/v1/admin/games/1/", json=game_data)
    assert response.status_code == 200
    changed_game = response.json()
    assert changed_game["name"] == game_data["name"]
    print("Тест 2 PUT")


@pytest.mark.asyncio
async def test_change_game_patch(create_some_games, login_admin_session):
    game_data = await create_partial_game()
    response = await login_admin_session.put("/api/v1/admin/games/1/", json=game_data)
    assert response.status_code == 200
    changed_game = response.json()
    assert changed_game["description"] == game_data["description"] and changed_game["rating"] == game_data["rating"]
    print("Тест 3 PATCH")

@pytest.mark.asyncio
async def test_delete_game(create_some_games, login_admin_session):
    response = await login_admin_session.delete("/api/v1/admin/games/1/")
    assert response.status_code == 204
    print("Тест 4 DELETE")

@pytest.mark.asyncio
async def test_get_games( create_some_games, login_admin_session):
    response = await login_admin_session.get("/api/v1/games/")
    assert response.status_code == 200
    print("Тест 5 GET ALL")


@pytest.mark.asyncio
async def test_create_admin( login_admin_session):

    response = await login_admin_session.get("/api/v1/admin/admin-only/")
    assert response.status_code == 200
    print("Тест 6 Создание Админа")




