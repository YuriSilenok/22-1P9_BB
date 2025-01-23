from peewee import Model, CharField, ForeignKeyField, DateTimeField, IntegerField, MySQLDatabase


mysql_db = MySQLDatabase('22-1p9bb', user='root', password='a2195966',
                         host='localhost', port=3306)

class Table(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = mysql_db


class User(Table):
    username = CharField()
    password = CharField()
    full_name = CharField()
    telegram = CharField()


class Organizator(Table):
    user = ForeignKeyField(User,on_delete = "CASCADE", on_update="CASCADE")


class Car(Table):
    color = CharField()
    number = CharField()


class Volunteer(Table):
    user = ForeignKeyField(User,on_delete = "CASCADE", on_update="CASCADE")
    car = ForeignKeyField(Car,on_delete = "CASCADE", on_update="CASCADE", null = True, default = None )



class Event(Table):
    name = CharField()
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    description = CharField()
    max_people = IntegerField()
    organizator = ForeignKeyField(Organizator,on_delete = "CASCADE", on_update="CASCADE")


class EventVolunteer(Table):
    event = ForeignKeyField(Event,on_delete = "CASCADE", on_update="CASCADE")
    volunteer = ForeignKeyField(Volunteer,on_delete = "CASCADE", on_update="CASCADE")


class Drive(Table):
    car = ForeignKeyField(Car,on_delete = "CASCADE", on_update="CASCADE")
    event_volunteer = ForeignKeyField(EventVolunteer,on_delete = "CASCADE", on_update="CASCADE")
    start_date_time = DateTimeField()
    start_location = CharField()
    max_passenger = IntegerField()


class PassengerStatus(Table):
    name = CharField()


class Passenger(Table):
    volunteer = ForeignKeyField(Volunteer,on_delete = "CASCADE", on_update="CASCADE")
    drive = ForeignKeyField(Drive,on_delete = "CASCADE", on_update="CASCADE")
    status = ForeignKeyField(PassengerStatus,on_delete = "CASCADE", on_update="CASCADE")


if __name__ == '__main__':

    with mysql_db:
        mysql_db.create_tables([
            User, Organizator, Car, Volunteer, Event, EventVolunteer, Drive, PassengerStatus, Passenger])







