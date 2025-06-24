from fastapi import APIRouter
from microshop.pages.games import router as products_pages_router

router = APIRouter()
router.include_router(products_pages_router, prefix="/pages")  # или другой префикс, если нужно