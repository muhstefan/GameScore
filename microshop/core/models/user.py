from sqlalchemy.orm import Mapped
from .base import Base


class User(Base):
    login: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]