from sqlalchemy import select

from gamescore.core.models import User


async def get_user_by_username(session, username: str):
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    return result.scalars().first()
