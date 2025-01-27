from fastapi import APIRouter, Depends, HTTPException
from app.schemas.event import EventCreate, EventResponse
from app.crud.event import create_event
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/events/", response_model=EventResponse)
async def create_event_endpoint(
    event: EventCreate,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "organizer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organizers can create events",
        )
    db_event = create_event(event, current_user["id"])
    return db_event