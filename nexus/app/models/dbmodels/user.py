from app.constants import META_TABLE_USER
from app.sqldb import MetaSQLDB
from app.utils.token import NexusToken


nt = NexusToken()

class User:

    def __init__(self, userid, password="", role=1):
        
        ##password by default empty, must be checked from higher function
        ##for a non empty password
        self.userid  = userid
        self.role = role
        self.password = nt.getMD5(password)
        self.apikey = nt.generateApiKey(self.userid)
        self.keyEnabled = 0

        ##other meta
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_USER

        ##all column names too? - Other names are included. will see, will be micro managing

    def insert(self):
        self.dbwrap.connect()
        ##ignore self.userid here
        ##user self.role and self.password
        ##insert self object into db
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        #print type(self.keyEnabled)
        query = "INSERT INTO " + META_TABLE_USER + " (userid, password, role, apikey, keyEnabled) \
                VALUES('%s', '%s', %d, '%s', %d)" % (self.userid, self.password, self.role,
                self.apikey, self.keyEnabled)

        print query
        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose()
        return numrows

    def delete(self):
        ##delete self object into db
        ##TODO - later
        pass

    def update(self, column='all'):
        ##update self object into db

        attr_list = ['all', 'password', 'role', 'keyEnabled']
        assert(column in attr_list)

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()
        base_query = "UPDATE " + META_TABLE_USER + " SET "
        rest_query = " WHERE userid= '"+str(self.userid) + "'"
        if column == "all":
            body_query = "password='%s', role=%d, apikey='%s', keyEnabled=%d" % \
                    (self.password, self.role, self.apikey, self.keyEnabled)
            query = base_query + body_query + rest_query
            print "UPDATE query"
            print query

        else:
            t = type(column)
            val = getattr(self, column)
            if t == int:
                typestr = "%d"
            else: typestr = "'%s'"
            if column == 'password':
                val = nt.getMD5(val)
            body_query = (column+"="+typestr) % (val)
            query = base_query + body_query + rest_query
            print "UPDATE query"
            print query

        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose()

        return numrows

    def setKeyEnabled(self, keyval):
        self.keyEnabled = keyval
        self.update(self, 'keyEnabled')
        return

    def validateUser(self, password):
        self.getSelfFromDB()
        password = nt.getMD5(password)
        if self.password == password:
            return True

        return False

    def __str__(self):
        print '[User: userid: '+str(self.userid)+' role: '+str(self.role)+']'
        return

    def getSelfFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT userid, password, role, apikey, keyEnabled \
                 FROM " + META_TABLE_USER + " where userid='" + str(self.userid) + "'"

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            uid = r[0]
            password = r[1]
            role = r[2]
            apikey = r[3]
            keyEnabled = r[4]

        self.password = password
        self.role = role
        self.apikey = apikey
        self.keyEnabled = keyEnabled
        self.dbwrap.commitAndClose()
        return self

    @classmethod
    def getUser(cls, userid):
        ##get User object using the userid
        ##has to be classmethod
        usr = User(userid)
        return usr.getSelfFromDB()

    def test(self):
        
        usr1 = User('amartya',)
