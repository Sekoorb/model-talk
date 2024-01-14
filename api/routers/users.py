from fastapi import APIRouter
from ..crud import create_user

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate):
    # ...
