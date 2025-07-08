from  fastapi import APIRouter

from microshop.api_v1.games.views import router as games_router
from microshop.api_v1.users.views import router as users_router
from microshop.api_v1.auth.views import router as auth_router

router = APIRouter()
router.include_router(router=games_router,prefix="/games")
router.include_router(router=users_router,prefix="/users")
router.include_router(router=auth_router,prefix="/auth")