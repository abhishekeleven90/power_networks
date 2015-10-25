from peewee import *
from app import app

##it is just the object it has not been connected!
mysqldb = MySQLDatabase(app.config['MYSQLDBNAME'], user = app.config['MYSQLDBUSER'], 
    password=app.config['MYSQLDBPASSWORD'])

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = mysqldb

class Person(BaseModel):
    name = CharField()

    class Meta:
        db_table = 'person'

class Pet(BaseModel):
    ownerid = ForeignKeyField(db_column='ownerid', rel_model=Person, to_field='id')
    type = CharField()

    class Meta:
        db_table = 'pet'

class Users(BaseModel):
    password = CharField(null=True)
    role = IntegerField(null=True)
    userid = CharField(primary_key=True)

    class Meta:
        db_table = 'users'


##it is just the dbobject
def dbobject():
    return mysqldb