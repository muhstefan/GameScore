from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gamescore.core.entities.users import UserCreate, UserUpdate, UserCreateDB
from gamescore.core.models import db_helper, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def prepare_user_create(user_in: UserCreate) -> UserCreateDB:
    hashed_password = hash_password(user_in.password)
    return UserCreateDB(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password
    )


async def prepare_user_update(
        user_id: int,
        user_update: UserUpdate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    update_data = user_update.model_dump(exclude_unset=True)

    # Проверка уникальности username
    if "username" in update_data:
        existing_user = await session.execute(
            select(User).where(User.username == update_data["username"], User.id != user_id)
        )
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой Логин уже есть"
            )

    # Хеширование пароля
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    return update_data
