from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    telegram: str
    role: str

class UserResponse(BaseModel):
    username: str
    full_name: str
    telegram: str
    role: str