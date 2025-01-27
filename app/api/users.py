from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate):
    db_user = create_user(user)
    return db_user