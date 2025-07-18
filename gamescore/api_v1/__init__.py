from  fastapi import APIRouter

from gamescore.api_v1.games.views import router as games_router
from gamescore.api_v1.users.views import router as users_router
from gamescore.api_v1.users.views_user_games import router as user_games_router
from gamescore.api_v1.auth.views import router as auth_router
from gamescore.api_v1.admin.views import router as admin_router
from gamescore.api_v1.rawg.views import router as rawg_router


router = APIRouter()
router.include_router(router=games_router,prefix="/games")
router.include_router(router=users_router,prefix="/users")
router.include_router(router=user_games_router,prefix="/users")
router.include_router(router=auth_router,prefix="/auth")
router.include_router(router=admin_router,prefix="/admin")
router.include_router(router=rawg_router,prefix="/rawg")