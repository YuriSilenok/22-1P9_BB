from fastapi import FastAPI
from app.api import users, events, drives

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(drives.router)