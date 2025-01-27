from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse

def create_event(event: EventCreate, user_id: int):
    db_event = Event.create(
        name=event.name,
        start_date_time=event.start_date_time,
        end_date_time=event.end_date_time,
        description=event.description,
        max_people=event.max_people,
        user_id=user_id,
    )
    return db_event