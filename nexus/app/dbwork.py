from peewee import *
from app import app
import pandas as pd
import MySQLdb as db

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

class Uuidtable(BaseModel):
    name = CharField(null=True)
    uuid = BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'uuidtable'



##it is just the dbobject
def dbobject():
    return mysqldb


def sqlQuerytoDF(query,ipaddress,database,user,password):
    database = db.connect(ipaddress, user, password, database)
    df = pd.read_sql(query, database)
    return df
#df = sqlQuerytoDF("select * from political_crawl_jan where mynetaid = 1","localhost","crawldb","root","yoyo")
#df['name'][0]

def createUuid(name):
    mydb = db.connect(app.config['MYSQLDBHOST'],app.config['MYSQLDBUSER'], 
        app.config['MYSQLDBPASSWORD'],app.config['MYSQLDBNAME'] )
    cursor = mydb.cursor()

    ##TODO: get uuidtable in constant config file 
    cursor.execute("insert into uuidtable(name) values('"+name+"');")
    mydb.commit()

    mydb.close()

    return cursor.lastrowid
