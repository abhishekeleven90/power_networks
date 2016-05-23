from peewee import *
from app import app
import pandas as pd
import MySQLdb as db
import shlex,subprocess

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


##generic can be used by anyone
def updateSQL(query,ipaddress,database,user,password):
    import MySQLdb
    # Open database connection
    db = MySQLdb.connect(ipaddress,user,password,database)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    numrows = cursor.execute(query);
    
    db.commit()

    db.close()
    
    return numrows

##to be used when updating resolved status in a crawled db
##TODO: since only for crawled db, need to remove the database? 
def updateResolved(tablename, row_id,ipaddress,database,user,password,resolved=1):

    ##need to modularize and move this code from here! : TODO!
    numrows = updateSQL("UPDATE "+tablename+" SET resolved="+str(resolved)+" WHERE id="+str(row_id)+";",ipaddress,database,user,password)
    print "UPDATE "+tablename+" SET resolved="+str(resolved)+" WHERE id="+str(row_id)+";"
    return numrows

# Delete all records of power_nexus db entities table
def del_all_index():
	import MySQLdb

	db = MySQLdb.connect("10.237.27.67","root","yoyo","power_nexus")
	cursor = db.connect()
	cursor.execute('TRUNCATE TABLE entities')
	db.commit()
	db.close()
	return

# Fill the power_nexus from csv
def fill_table():
    ##Assuming entities.csv is in current folder
    cmd = "mysqlimport --ignore-lines=1 \
            --fields-terminated-by=, --columns='uuid,name,labels,aliases,keywords' \
            --local -u root -p power_nexus entities.csv"

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return

#Add new entry to power_nexus db
def add_entry(datavalues = None):
	import MySQLdb

	if not datavalues:
		print "Value Error"
		return

	if type(datavalues) != dict:
		print "Non dict arg"
		return

	db = MySQLdb.connect("10.237.27.67","root","yoyo","power_nexus")
	cursor = db.connect()
	numrows = cursor.execute("INSERT INTO entities(uuid,name,labels,aliases,keywords)\
					VALUES ('%s','%s','%s','%s')",\
					(datavalues['uuid'],datavalues['name'],datavalues['labels'],datavalues['aliases'],datavalues['keywords']))
	db.commit()
	db.close()
	return numrows


if __name__ == "__main__":
	del_all_index()
