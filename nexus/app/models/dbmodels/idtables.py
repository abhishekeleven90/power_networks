import MySQLdb as mysqldb
from app.sqldb import MetaSQLDB

class Entity:

    ## CREATE TABLE uuidtable(uuid int NOT NULL PRIMARY KEY ,name varchar( 3000 ));
    ## mysqlimport --ignore-lines=1 --fields-terminated-by=, --columns='uuid,name' --local -u root -p flasktemp uuidtable.csv
    ## MOST IMP THING while importing: keep the csvname same as tablename
    ## keeping int now
    ## match (n:entity) return n.uuid as uuid, n.name as name

    def __init__(self, name):
        self.uuid = None
        self.name = name ##TODO: but what if the primary name changes?
        #self.uri = uri #TODO: will decide afterwards 
        from app.constants import META_TABLE_UUID
        self.tablename  = META_TABLE_UUID
        self.dbwrap = MetaSQLDB()

    def create(self):
        query = 'insert into uuidtable(name) values("%s");'
        query = query %(self.name)
        

        cursor = self.dbwrap.connectAndCursor()
        numrows = cursor.execute(query)
        self.uuid =  cursor.lastrowid
        self.dbwrap.commitAndClose() ##what if something breaks? TODO!

        return numrows

class Link: ##chossing this name instead of a relation
    ## startnode and ennode can be foregin keys here constraints
    ## finally the table query! 
    ## create table relidtable(relid int not null primary key, reltype varchar(1000), startuuid int, enduuid int, foreign key (startuuid) references uuidtable(uuid) on delete cascade on update cascade,  foreign key (enduuid) references uuidtable(uuid) on delete cascade on update cascade); 
    ## mysqlimport --ignore-lines=1 --fields-terminated-by=, --columns='relid,reltype,startuuid,enduuid' --local -u root -p flasktemp relidtable.csv
    ## match (start:entity)-[r]->(end:entity) return r.relid as relid, type(r) as reltype, start.uuid as startuuid, end.uuid as enduuid


    def __init__(self, reltype, startuuid, enduuid):

        self.relid = None ##this helps in tracking bugs really! 
        self.reltype = reltype ##RULE: once a type given to a relation, it's always given
        self.startuuid = startuuid
        self.enduuid = enduuid
        from app.constants import META_TABLE_RELID
        self.tablename  = META_TABLE_RELID
        self.dbwrap = MetaSQLDB()

    def create(self):
        query = "insert into relidtable(reltype, startuuid, enduuid ) values('%s', %s, %s);" ##TODO use constant name of table? here?
        query = query %(self.reltype, self.startuuid, self.enduuid)
        

        cursor = self.dbwrap.connectAndCursor()
        numrows = cursor.execute(query)
        self.relid =  cursor.lastrowid
        self.dbwrap.commitAndClose()

        print numrows

class HyperEdgeNode:

    # CREATE TABLE henidtable(
    # henid bigint( 20 ) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    # labels text
    # )

    def __init__(self, labels): 
        ##for the sake of completion for now just writing the labels for now for this

        self.henid = None
        self.labels = labels ##TODO: Comma separated list
        from app.constants import META_TABLE_HENID
        self.tablename  = META_TABLE_HENID
        self.dbwrap = MetaSQLDB()

    def create(self):
        query = "insert into henidtable(labels) values('%s');" ##TODO use constant name of table? here?
        query = query %(self.labels)
        

        cursor = self.dbwrap.connectAndCursor()
        numrows = cursor.execute(query)
        self.henid =  cursor.lastrowid
        self.dbwrap.commitAndClose() ##what if something breaks? TODO!

        print numrows    

