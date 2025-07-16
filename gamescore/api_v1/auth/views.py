from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, Cookie, Response,APIRouter
from gamescore.api_v1.auth.security import verify_password, generate_and_set_tokens, decode_jwt_token
from gamescore.api_v1.auth.config import Production
from gamescore.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.api_v1.auth.crud import get_user_by_username


router = APIRouter(tags=["Auth"])



@router.post("/login/")
async def login(response: Response,
                form_data: OAuth2PasswordRequestForm = Depends(),
                session : AsyncSession = Depends(get_db)):
    user = await get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    generate_and_set_tokens(response, str(user.id), secure=Production)

    return {"message": "Logged in successfully"}


@router.post("/refresh/")
async def refresh_token(
        response: Response,
        refresh_token: str | None = Cookie(default=None)
):
    user_id = decode_jwt_token(refresh_token)
    generate_and_set_tokens(response, str(user_id), secure=Production)

    return {"message": "Access and refresh tokens refreshed"}


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True, samesite="lax", secure=Production)
    response.delete_cookie(key="refresh_token", httponly=True, samesite="lax", secure=Production)
    return {"message": "Logged out successfully"}