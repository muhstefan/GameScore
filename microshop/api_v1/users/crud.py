from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from microshop.core.models import User
from sqlalchemy.engine import Result
from sqlalchemy import select
from microshop.core.models.users import UserUpdate, UserCreateDB

async def get_users(session : AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result : Result = await session.execute(stmt)
    users = result.scalars().all()  # scalars аналог **
    return list(users)

async def get_user(session: AsyncSession,user_id: int)-> User | None:
    return await session.get(User, user_id)

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