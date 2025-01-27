from peewee import CharField, ForeignKeyField
from .base import Table

class User(Table):
    username = CharField(unique=True)
    password = CharField()
    full_name = CharField()
    telegram = CharField()
    role = CharField()  # "volunteer" or "organizer"