from fastapi import APIRouter,Depends,Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response


from gamescore.api_v1.auth.security import *
from gamescore.api_v1.auth.config import Production
from gamescore.core.db import get_db

router = APIRouter(tags=["Auth"])

def set_auth_cookies(response: Response, access_token: str, refresh_token: str, secure: bool):
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=secure,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=secure,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )


@router.post("/login/")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), session : AsyncSession = Depends(get_db)):
    user = await get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    set_auth_cookies(response, access_token, refresh_token, secure=Production)

    return {"message": "Logged in successfully"}


@router.post("/refresh/")
async def refresh_token(
        response: Response,
        session: AsyncSession = Depends(get_db),
        refresh_token: str | None = Cookie(default=None)
):
    user = await validate_refresh_token_and_get_user(session, refresh_token)

    new_access_token = create_access_token(data={"sub": user.username})
    new_refresh_token = create_refresh_token(data={"sub": user.username})

    set_auth_cookies(response, new_access_token, new_refresh_token, secure=Production)

    return {"message": "Access and refresh tokens refreshed"}


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True, samesite="lax", secure=Production)
    response.delete_cookie(key="refresh_token", httponly=True, samesite="lax", secure=Production)
    return {"message": "Logged out successfully"}