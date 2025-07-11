from fastapi import APIRouter, Depends
from microshop.api_v1.auth.security import require_admin


router = APIRouter(tags=["Admin"])

@router.get("/admin-only")
async def admin_only_endpoint(current_admin_user = Depends(require_admin)):
    return {"message": f"Привет, {current_admin_user.username}! Это эндпоинт только для админов."}
