from app.constants import META_TABLE_CHANGE
from app.sqldb import MetaSQLDB
from datetime import datetime

class ChangeItem:

    def __init__(self, taskid=None, pushedby='', verifiedby='', 
            fetchdate='', pushdate=''):
        
        ##password by default empty, must be checked from higher function
        ##for a non empty password
        self.changeid = None
        self.taskid  = taskid
        self.pushedby = pushedby
        self.verifiedby = verifiedby
        self.verifydate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.fetchdate = fetchdate
        self.pushdate = pushdate

        ##other meta
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_CHANGE

        ##all column names too? - Other names are included. will see, will be micro managing

    def insert(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[ChangeID object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        #print type(self.keyEnabled)
        query = "INSERT INTO " + self.tablename + " (taskid, pushedby, verifiedby,\
                verifydate, fetchdate, pushdate) VALUES(%d, '%s', '%s', '%s', '%s','%s')"\
                % (self.taskid, self.pushedby, self.verifiedby, self.verifydate,
                        self.fetchdate, self.pushdate)

        print query
        numrows = cursor.execute(query)
        self.changeid = cursor.lastrowid
        self.dbwrap.commitAndClose()
        return numrows

    def delete(self):
        ##delete self object into db
        ##TODO - later
        pass

    
    def __str__(self):
        s = '[Change: changeid: '+str(self.changeid)+' pushedby: '+str(self.pushedby)+']'
        print s
        return s

    def getSelfFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT changeid, taskid, pushedby, verifiedby, verifydate, \
                 pushdate, fetchdate FROM " + self.tablename + " where changeid=" + str(self.changeid)

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.changeid = r[0]
            self.taskid = r[1]
            self.pushedby = r[2]
            self.verifiedby = r[3]
            self.verifydate = r[4]
            self.pushdate = r[5]
            self.fetchdate = r[6]

        return self

    @classmethod
    def getChangeItem(cls, changeid):
        chg = ChangeItem()
        chg.changeid = changeid
        return chg.getSelfFromDB()

