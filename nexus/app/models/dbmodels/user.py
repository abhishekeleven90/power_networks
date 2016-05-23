from app.constants import META_TABLE_USER
import MySQLdb as mysqldb
from app.sqldb import MetaSQLDB

class User:

    def __init__(self, userid, role, password):
        
        ##column variables
        self.userid  = userid
        self.role = role
        self.password = password

        ##other meta
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_USER

        ##all column names too? will see, will be micro managing

    def insert(self):
        ##ignore self.userid here
        ##user self.role and self.password
        ##insert self object into db
        pass

    def delete(self):
        ##delete self object into db
        pass

    def update(self):
        ##update self object into db
        pass

    def __str__():
        print '[User: userid: '+str(userid)+' role: '+str(role)']'

    @classmethod
    def getUser(cls, userid):
        ##get User object using the userid
        ##has to be classmethod
        pass

    def test(self):
        pass
