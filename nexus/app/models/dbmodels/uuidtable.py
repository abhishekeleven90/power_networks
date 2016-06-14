import MySQLdb as mysqldb
from app.sqldb import MetaSQLDB

class UUIDTable:

    ## CREATE TABLE uuidtable(uuid int NOT NULL PRIMARY KEY ,name varchar( 3000 ));
    ## mysqlimport --ignore-lines=1 --fields-terminated-by=, --columns='uuid,name' --local -u root -p flasktemp uuidtable.csv
    ## MOST IMP THING while importing: keep the csvname same as tablename
    ## keeping int now
    ## match (n:entity) return n.uuid as uuid, n.name as name

    def __init__(self, name, uuid):
        self.uuid = uuid
        self.name = name ##TODO: but what if the primary name changes?
        #self.uri = uri #TODO: will decide afterwards
        from app.constants import META_TABLE_UUID
        self.tablename  = META_TABLE_UUID
        self.dbwrap = MetaSQLDB()

    def create(self):
        query = "insert into uuidtable(uuid, name) values(%s,'%s');"
        query = query %(self.uuid, self.name)

        cursor = self.dbwrap.connectAndCursor()
        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose() ##what if something breaks? TODO!

        return numrows
