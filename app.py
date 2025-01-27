from datetime import datetime, timedelta, timezone
from typing import Annotated
from models import User, Car, UserCar, Event, EventVolunteer
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserDATA(BaseModel):
    username: str
    telegram: str | None = None
    full_name: str | None = None
    role: str  # "volunteer" or "organizer"

class UserInDB(UserDATA):
    password: str

class UserCreate(UserDATA):
    password: str

class EventCreate(BaseModel):
    name: str
    start_date_time: datetime
    end_date_time: datetime
    description: str
    max_people: int

class EventResponse(BaseModel):
    id: int
    name: str
    start_date_time: datetime
    end_date_time: datetime
    description: str
    max_people: int
    user: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    user = User.get_or_none(username=username)
    if user:
        return UserInDB(
            username=user.username,
            telegram=user.telegram,
            full_name=user.full_name,
            role=user.role,
            password=user.password,
        )

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserDATA, Depends(get_current_user)],
):
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=UserDATA)
async def read_users_me(
    current_user: Annotated[UserDATA, Depends(get_current_active_user)],
):
    return current_user

@app.post("/register/", response_model=UserDATA)
async def register_user(user: UserCreate):
    existing_user = User.get_or_none(username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    db_user = User.create(
        username=user.username,
        password=hashed_password,
        full_name=user.full_name,
        telegram=user.telegram,
        role=user.role,
    )
    return UserDATA(
        username=db_user.username,
        full_name=db_user.full_name,
        telegram=db_user.telegram,
        role=db_user.role,
    )

@app.post("/events/", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    current_user: Annotated[UserDATA, Depends(get_current_active_user)],
):
    if current_user.role != "organizer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organizers can create events",
        )
    user = User.get_or_none(username=current_user.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not found",
        )

    db_event = Event.create(
        name=event.name,
        start_date_time=event.start_date_time,
        end_date_time=event.end_date_time,
        description=event.description,
        max_people=event.max_people,
        user=user,
    )
    return EventResponse(
        id=db_event.id,
        name=db_event.name,
        start_date_time=db_event.start_date_time,
        end_date_time=db_event.end_date_time,
        description=db_event.description,
        max_people=db_event.max_people,
        user=user.username,
    )

@app.post("/events/{event_id}/register/")
async def register_for_event(
    event_id: int,
    current_user: Annotated[UserDATA, Depends(get_current_active_user)],
):
    event = Event.get_or_none(id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    user= User.get_or_none(username= current_user.username)
    EventVolunteer.create(event=event, user=user)
    return {"message": "Successfully registered for the event"}