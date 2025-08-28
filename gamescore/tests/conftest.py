import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from gamescore.api_v1.users.dependencies import hash_password
from gamescore.core.db import get_db
from gamescore.core.models import User, DataBaseHelper
from gamescore.main import app
from .utils import create_random_game
from ..api_v1.auth import config


@pytest_asyncio.fixture(loop_scope="module")
def postgres_container():
    with PostgresContainer("postgres:17-alpine") as postgres:
        postgres.driver = "+asyncpg"  # Правильный драйвер asyncpg
        yield postgres


@pytest_asyncio.fixture(loop_scope="module")
def test_db_helper(postgres_container):
    return DataBaseHelper(url=postgres_container.get_connection_url(), echo=False)


@pytest_asyncio.fixture(loop_scope="module")
async def override_get_db(test_db_helper):
    async def _override():
        async for session in test_db_helper.session_dependency():
            yield session

    return _override


@pytest_asyncio.fixture(loop_scope="module")
async def async_client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def prepare_test_db_per_function(test_db_helper):
    print("Очистка и подготовка базы перед тестом")
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

@pytest_asyncio.fixture(loop_scope="module")
async def create_some_games(login_admin_session):
    print("Заполняем играми")
    games = []
    for _ in range(5):
        game_data = await create_random_game()
        response = await login_admin_session.post("/api/v1/admin/games/", json=game_data)
        assert response.status_code == 201
        games.append(response.json())
    return games


@pytest_asyncio.fixture(loop_scope="module")
async def create_admin(test_db_helper):
    async for session in test_db_helper.session_dependency():
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


@pytest_asyncio.fixture(loop_scope="module")
async def login_admin_session(async_client, create_admin):
    # Логинимся под созданным админом
    login_response = await async_client.post("/api/v1/auth/login/",
                                             data={"username": create_admin.username, "password": "admin"},
                                             # create_admin.username фикстура что то возвращает и мы к ней обращаемся
                                             headers={"Content-Type": "application/x-www-form-urlencoded"}
                                             )
    assert login_response.status_code == 200
    return async_client