from gamescore.main import app
from gamescore.core.db import get_db  # ваша функция-зависимость
from test_db_helper import db_helper_test  # ваш тестовый db_helper
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from utils import create_random_game

# Переопределяем сессию для подключения к тестовой бд
async def override_get_db():
    async for session in db_helper_test.session_dependency():
        yield session


# Делать запросы к СУЩЕСТВУЮЩЕМУ ПРИЛОЖЕНИЮ , поэтому на основе мы его не юзаем
@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function", autouse=True) # scope Запускать каждый раз перед тестами, auto-use автоматически.
async def prepare_test_db_per_function():
    print("Очистка и подготовка базы перед тестом")
    # 1. Удаляем все таблицы
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    # 2. Создаем все таблицы заново
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def create_some_games(async_client):
    print("Заполняем играми")
    games = []
    for _ in range(5):
        game_data = await create_random_game()
        response = await async_client.post("/api/v1/games/", json=game_data)
        assert response.status_code == 201
        games.append(response.json())
    return games
