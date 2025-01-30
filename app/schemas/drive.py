from datetime import datetime
from pydantic import BaseModel

class DriveCreate(BaseModel):
    car_id: int  # ID автомобиля, который будет использоваться для поездки
    event_volunteer_id: int  # ID записи EventVolunteer, связанной с поездкой
    start_date_time: datetime  # Дата и время начала поездки
    start_location: str  # Место отправления
    max_passenger: int  # Максимальное количество пассажиров

class DriveResponse(BaseModel):
    id: int  # ID поездки
    car_id: int  # ID автомобиля
    event_volunteer_id: int  # ID записи EventVolunteer
    start_date_time: datetime  # Дата и время начала поездки
    start_location: str  # Место отправления
    max_passenger: int  # Максимальное количество пассажиров

    class Config:
        from_attributes = True  # Ранее использовалось `orm_mode = True` в Pydantic v1