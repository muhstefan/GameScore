from gamescore.core.config import BASE_DIR, Settings
from gamescore.core.models import DataBaseHelper



class SettingsTest(Settings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/test_db.sqlite3"

test_settings = SettingsTest()

# Создаем тестовый db_helper по образу основного
db_helper_test = DataBaseHelper(
    url=test_settings.db_url,
    echo=test_settings.db_echo
)
