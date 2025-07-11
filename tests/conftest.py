from gamescore.main import app
from gamescore.core.models import User
from gamescore.api_v1.users.dependencies import hash_password
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


# Делать запросы к СУЩЕСТВУЮЩЕМУ ПРИЛОЖЕНИЮ, поэтому на основе мы его не юзаем
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


@pytest_asyncio.fixture
async def create_admin():
    async for session in db_helper_test.session_dependency(): #т.к обращаемся к бд а не к клиенту
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin"),
            role="admin"
        )
        session.add(admin_user)
        await session.commit()
        await session.refresh(admin_user)
        yield admin_user
        break  # чтобы выйти из генератора сессии

@pytest_asyncio.fixture
async def login_admin(async_client, create_admin):
    # Логинимся под созданным админом
    login_response = await async_client.post("/api/v1/auth/login/",
        data={"username": create_admin.username, "password": "admin"},  # create_admin.username фикстура что то возвращает и мы к ней обращаемся
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    print(async_client.cookies)
