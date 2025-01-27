from peewee import ForeignKeyField
from .base import Table
from .user import User
from .event import Event

class EventVolunteer(Table):
    event = ForeignKeyField(Event, on_delete="CASCADE", on_update="CASCADE")
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто записался на мероприятие