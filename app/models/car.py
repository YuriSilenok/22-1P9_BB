from peewee import CharField
from .base import Table

class Car(Table):
    color = CharField()
    number = CharField()