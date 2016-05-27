
class SQLDB:
    
    def __init__(self, dbname, dbhost, dbuser, dbpass, dbport):
        self.dbname = dbname
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbport = dbport
        ##for all the other methods just call connect do work,
        ##close, commit, etc.
        
    def connect(self):
        import MySQLdb as mysqldb
        self.sqldbobj = mysqldb.connect(host = self.dbhost, user = self.dbuser, passwd = self.dbpass, db =  self.dbname, port = self.dbport)

    def commitAndClose(self):
        self.sqldbobj.commit()
        self.sqldbobj.close()

    def cursor(self):
        self.cur =  self.sqldbobj.cursor()
        return self.cur

    def connectAndCursor(self):
        import MySQLdb as mysqldb
        self.sqldbobj = mysqldb.connect(host = self.dbhost, user = self.dbuser, passwd = self.dbpass, db =  self.dbname, port = self.dbport)
        self.cur =  self.sqldbobj.cursor()
        return self.cur        

    ##TODO: execute method?

    ##generic can be used by anyone
    ##returns number of rows@
    def updateSQL(self, query):
        import MySQLdb as mysqldb
        # Open database connection
        db = mysqldb.connect(self.dbhost, self.dbuser, self.password, self.dbname)
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # execute SQL query using execute() method.
        numrows = cursor.execute(query);
        db.commit()
        db.close()
        return numrows

def sqlQuerytoDF(self, query,ipaddress,d):
        import pandas as pd
        db = mysqldb.connect(self.dbhost, self.dbuser, self.password, self.dbname)
        df = pd.read_sql(query, db)
        return df

class MetaSQLDB(SQLDB):

    def __init__(self):
        from constants import META_SQL_DBHOST, META_SQL_DBNAME, META_SQL_DBPASSWORD, META_SQL_DBUSER, META_SQL_DBPORT
        SQLDB.__init__(self, META_SQL_DBNAME, META_SQL_DBHOST, META_SQL_DBUSER, META_SQL_DBPASSWORD, META_SQL_DBPORT)

    def metamethods(self):
        pass


class IndexSQLDB(SQLDB):

    def __init__(self):
        from constants import INDEX_SQL_DBHOST, INDEX_SQL_DBNAME, INDEX_SQL_DBPASSWORD, INDEX_SQL_DBUSER, INDEX_SQL_DBPORT    
        SQLDB.__init__(self, INDEX_SQL_DBNAME, INDEX_SQL_DBHOST, INDEX_SQL_DBUSER, INDEX_SQL_DBPASSWORD, INDEX_SQL_DBPORT)

    def indexmethods(self):
        pass







