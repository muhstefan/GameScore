from  fastapi import APIRouter

from microshop.api_v1.games.views import router as games_router

router = APIRouter()
router.include_router(router=games_router,prefix="/games")