from fastapi import APIRouter, Depends

from gamescore.api_v1.auth.dependencies import require_admin
from .views_games import router as games_router
from .views_users import router as users_router

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/admin-only/")
async def admin_only_endpoint(current_admin_user=Depends(require_admin)):
    return {"message": f"Привет, {current_admin_user.username}! Это эндпоинт только для админов."}


router.include_router(users_router)
router.include_router(games_router)
