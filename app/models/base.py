from peewee import Model, CharField, ForeignKeyField, DateTimeField, IntegerField, MySQLDatabase

mysql_db = MySQLDatabase('22-1p9bb', user='root', password='a2195966',
                         host='localhost', port=3306)

class Table(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = mysql_db