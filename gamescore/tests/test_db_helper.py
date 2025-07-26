import os

from gamescore.core.config import Settings
from gamescore.core.models import DataBaseHelper


class SettingsTest(Settings):
    db_url: str = os.getenv("test_db_url")


test_settings = SettingsTest()

# Создаем тестовый db_helper по образу основного
db_helper_test = DataBaseHelper(
    url=test_settings.db_url,
    echo=test_settings.db_echo
)
