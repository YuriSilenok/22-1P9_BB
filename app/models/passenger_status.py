from peewee import CharField
from .base import Table

class PassengerStatus(Table):
    name = CharField()