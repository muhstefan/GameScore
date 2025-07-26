from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = "postgresql+asyncpg://postgres:test@localhost:5432/main_db"
    db_echo: bool = False


settings = Settings()  # Создаем объект класса выше
