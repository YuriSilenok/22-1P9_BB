from peewee import ForeignKeyField, DateTimeField, CharField, IntegerField
from .base import Table
from .car import Car
from .event_volunteer import EventVolunteer

class Drive(Table):
    car = ForeignKeyField(Car, on_delete="CASCADE", on_update="CASCADE")
    event_volunteer = ForeignKeyField(EventVolunteer, on_delete="CASCADE", on_update="CASCADE")
    start_date_time = DateTimeField()
    start_location = CharField()
    max_passenger = IntegerField()