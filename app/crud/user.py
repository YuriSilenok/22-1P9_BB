from app.models.user import User
from app.schemas.user import UserCreate

def create_user(user: UserCreate):
    db_user = User.create(**user.dict())
    return db_user