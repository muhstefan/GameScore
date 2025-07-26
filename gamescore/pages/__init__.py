from fastapi import APIRouter

from gamescore.pages.games import router as products_pages_router
from gamescore.pages.home import router as home_page_router
from gamescore.pages.login import router as login_pages_router
from gamescore.pages.me import router as me_page_router
from gamescore.pages.my_games import router as me_games_catalog_router

router = APIRouter(tags=["Pages"])

router.include_router(products_pages_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(login_pages_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(home_page_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(me_page_router, prefix="/pages")  # или другой префикс, если нужно
router.include_router(me_games_catalog_router, prefix="/pages")  # или другой префикс, если нужно
