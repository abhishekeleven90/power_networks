import MySQLdb as mysqldb
from app.sqldb import MetaSQLDB

class RELIDTable: ##chossing this name instead of a relation
    ## startnode and ennode can be foregin keys here constraints
    ## finally the table query! 
    ## create table relidtable(relid int not null primary key, reltype varchar(1000), startuuid int, enduuid int, foreign key (startuuid) references uuidtable(uuid) on delete cascade on update cascade,  foreign key (enduuid) references uuidtable(uuid) on delete cascade on update cascade); 
    ## mysqlimport --ignore-lines=1 --fields-terminated-by=, --columns='relid,reltype,startuuid,enduuid' --local -u root -p flasktemp relidtable.csv
    ## match (start:entity)-[r]->(end:entity) return r.relid as relid, type(r) as reltype, start.uuid as startuuid, end.uuid as enduuid


    def __init__(self, relid, reltype, startuuid, enduuid):

        self.relid = relid ##this helps in tracking bugs really! 
        self.reltype = reltype ##RULE: once a type given to a relation, it's always given
        self.startuuid = startuuid
        self.enduuid = enduuid
        from app.constants import META_TABLE_RELID
        self.tablename  = META_TABLE_RELID
        self.dbwrap = MetaSQLDB()

    def create(self):
        query = "insert into relidtable(relid, reltype, startuuid, enduuid ) values(%s,'%s', %s, %s);" 
        ##TODO use constant name of table? here?

        query = query %(self.relid, self.reltype, self.startuuid, self.enduuid)
        
        cursor = self.dbwrap.connectAndCursor()
        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose()

        ##TODO: what about databse errors? how to catch them

        print numrows