import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel


from gamescore.api_v1.users.dependencies import hash_password
from gamescore.core.db import get_db
from gamescore.core.models import User
from gamescore.main import app
from .test_db_helper import db_helper_test
from .utils import create_random_game



async def override_get_db():
    async for session in db_helper_test.session_dependency():
        yield session




# Делать запросы к СУЩЕСТВУЮЩЕМУ ПРИЛОЖЕНИЮ, поэтому на основе мы его не юзаем
@pytest_asyncio.fixture(scope="module")
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_test_db_per_function():
    print("Очистка и подготовка базы перед тестом")
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="module")
async def create_some_games(login_admin_session):
    print("Заполняем играми")
    games = []
    for _ in range(5):
        game_data = await create_random_game()
        response = await login_admin_session.post("/api/v1/admin/games/", json=game_data)
        assert response.status_code == 201
        games.append(response.json())
    return games


@pytest_asyncio.fixture(scope="module")
async def create_admin():
    async for session in db_helper_test.session_dependency():
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


@pytest_asyncio.fixture(scope="module")
async def login_admin_session(async_client, create_admin):
    # Логинимся под созданным админом
    login_response = await async_client.post("/api/v1/auth/login/",
                                             data={"username": create_admin.username, "password": "admin"},
                                             # create_admin.username фикстура что то возвращает и мы к ней обращаемся
                                             headers={"Content-Type": "application/x-www-form-urlencoded"}
                                             )
    assert login_response.status_code == 200
    return async_client