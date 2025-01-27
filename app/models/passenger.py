from peewee import ForeignKeyField
from .base import Table
from .user import User
from .drive import Drive
from .passenger_status import PassengerStatus

class Passenger(Table):
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто является пассажиром
    drive = ForeignKeyField(Drive, on_delete="CASCADE", on_update="CASCADE")
    status = ForeignKeyField(PassengerStatus, on_delete="CASCADE", on_update="CASCADE")