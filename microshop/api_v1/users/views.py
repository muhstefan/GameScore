from fastapi import APIRouter
from microshop.api_v1.users.schemas import UserCreate
import microshop.api_v1.users.crud as crud

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/")
def create_user(user: UserCreate):
    return crud.create_user(user_in=user)
