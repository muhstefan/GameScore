from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from sqlalchemy.orm import selectinload

from gamescore.core.models import User
from sqlalchemy.engine import Result
from sqlalchemy import select
from gamescore.core.models.users import UserCreateDB
from gamescore.api_v1.games.crud import get_game

async def get_users(session : AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result : Result = await session.execute(stmt)
    users = result.scalars().all()  # scalars аналог **
    return list(users)

#Это метод пред загрузки пользователя И сразу всех его связей, так надо чтобы от ленивой загрузки не тормозить
async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User).options(selectinload(User.games)).where(User.id == user_id)
    )
    return result.scalars().first()

async def create_user(session: AsyncSession, user_data: UserCreateDB):
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user

async def update_user(
        session: AsyncSession,
        user_id: int,
        update_data: dict
) -> User:
    user = await get_user(session, user_id)
    for name, value in update_data.items():
        setattr(user, name, value)
    await session.commit()
    return user

async def delete_user(session: AsyncSession,
                      user_id: int
                      ) -> None:
    user = await get_user(session, user_id)
    await session.delete(user)
    await session.commit()

async def add_game_to_user(session: AsyncSession,
                           user_id: int,
                           game_id: int):
    user = await get_user(session, user_id)
    game = await get_game(session, game_id)
    if not user or not game:
        raise ValueError("Пользователь или игра не найдены")
    if game not in user.games:
        user.games.append(game)
        session.add(user)
        await session.commit()