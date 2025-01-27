from datetime import datetime
from pydantic import BaseModel

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