from peewee import Model, CharField, ForeignKeyField, DateTimeField, IntegerField, MySQLDatabase

mysql_db = MySQLDatabase('22-1p9bb', user='root', password='a2195966',
                         host='localhost', port=3306)

class Table(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = mysql_db

class User(Table):
    username = CharField(unique=True)
    password = CharField()
    full_name = CharField()
    telegram = CharField()
    role = CharField()  # "volunteer" or "organizer"
    owner = ForeignKeyField("self", on_delete="CASCADE", on_update="CASCADE")


class RegistrationCode(Table):
    owner = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")
    value = IntegerField()


class Role(Table):
    name = CharField()


class UserRole(Table):
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")
    role = ForeignKeyField(Role, on_delete="CASCADE", on_update="CASCADE")


class Car(Table):
    color = CharField()
    number = CharField()


# Транзитивная таблица для связи пользователя и автомобиля
class UserCar(Table):
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")
    car = ForeignKeyField(Car, on_delete="CASCADE", on_update="CASCADE")


class Event(Table):
    name = CharField()
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    description = CharField()
    max_people = IntegerField()
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто создал мероприятие

class EventVolunteer(Table):
    event = ForeignKeyField(Event, on_delete="CASCADE", on_update="CASCADE")
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто записался на мероприятие

class Drive(Table):
    car = ForeignKeyField(Car, on_delete="CASCADE", on_update="CASCADE")
    event_volunteer = ForeignKeyField(EventVolunteer, on_delete="CASCADE", on_update="CASCADE")
    start_date_time = DateTimeField()
    start_location = CharField()
    max_passenger = IntegerField()

class PassengerStatus(Table):
    name = CharField()

class Passenger(Table):
    user = ForeignKeyField(User, on_delete="CASCADE", on_update="CASCADE")  # Кто является пассажиром
    drive = ForeignKeyField(Drive, on_delete="CASCADE", on_update="CASCADE")
    status = ForeignKeyField(PassengerStatus, on_delete="CASCADE", on_update="CASCADE")

if __name__ == '__main__':
    with mysql_db:
        mysql_db.create_tables([
            User, Car, UserCar, Event, EventVolunteer, Drive, PassengerStatus, Passenger, RegistrationCode])