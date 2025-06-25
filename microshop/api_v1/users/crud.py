from sqlalchemy.ext.asyncio import AsyncSession # это сессия для работы с бд
from microshop.core.models import User
from sqlalchemy.engine import Result
from sqlalchemy import select
from microshop.core.models.user import UserCreate,UserUpdate


async def get_users(session : AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result : Result = await session.execute(stmt)
    users = result.scalars().all()  # scalars аналог **
    return list(users)

async def get_user(session: AsyncSession,user_id: int)-> User | None:
    return await session.get(User, user_id)

async def create_user(session: AsyncSession, user_in: UserCreate):
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user

async def update_user(session: AsyncSession,  #может полностью и частично обновлять объект
                         user: User,
                         user_update: UserUpdate | UserUpdatePartical,
                         partical : bool = False
                         )->User:
    for name, value in user_update.model_dump(exclude_unset=partical).items():
        setattr(user,name,value)
    await session.commit()
    return user

async def delete_user(session: AsyncSession,
                         user: User,

)-> None:
    await session.delete(user)
    await session.commit()