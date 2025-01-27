from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField
from .base import Table
from .user import User

class Event(Table):
    name = CharField()
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    description = CharField()
    max_people = IntegerField()
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто создал мероприятие