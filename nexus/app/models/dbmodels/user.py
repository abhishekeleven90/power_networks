from app.constants import META_TABLE_USER
from app.sqldb import MetaSQLDB
from app.utils.nexustoken import NexusToken


nt = NexusToken()

class User:

    def __init__(self, userid, password="", role=1, keyEnabled=0,
                 name='', lastlogin='', lastpwdchange=''):

        ##password by default empty, must be checked from higher function
        ##for a non empty password
        self.userid  = userid
        self.role = role
        self.password = nt.getMD5(password)
        self.apikey = nt.generateApiKey(self.userid)
        self.keyEnabled = keyEnabled
        self.name = name
        # lastlogin and lastpwdchange are normally inserted
        # during last login last pwd change only
        self.lastlogin = lastlogin
        self.lastpwdchange = lastpwdchange

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
        query = "INSERT INTO " + self.tablename + " (userid, password, role, apikey,\
                 keyEnabled, name, lastlogin, lastpwdchange) VALUES('%s', '%s', %d, '%s', %d, '%s', '%s', '%s')"\
                 % (self.userid, self.password, self.role, self.apikey, self.keyEnabled,
                    self.name, self.lastlogin, self.lastpwdchange)

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

        attr_list = ['all', 'password', 'role', 'keyEnabled'
                     'name', 'lastpwdchange', 'lastlogin']
        assert(column in attr_list)

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()
        base_query = "UPDATE " + self.tablename + " SET "
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
        #self.getSelfFromDB()
        password = nt.getMD5(password)
        if self.password == password:
            return True

        return False

    @classmethod
    def validateToken(cls, userid, token):
        try:
            usr = cls.getUser(userid=userid)
            return usr.apikey==token and usr.keyEnabled==1
        except Exception as e:
            return False
        pass


    def __str__(self):
        print '[User: userid: '+str(self.userid)+' role: '+str(self.role)+']'
        return

    def getSelfFromDB(self):
        ''' Gets an user obj by userid field'''

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT userid, password, role, apikey, keyEnabled \
                 , name, lastlogin, lastpwdchange FROM " + self.tablename\
                + " where userid='" + str(self.userid) + "'"

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.userid = r[0]
            self.password = r[1]
            self.role = r[2]
            self.apikey = r[3]
            self.keyEnabled = r[4]
            self.name = r[5]
            self.lastlogin = r[6]
            self.lastpwdchange = r[7]

        self.dbwrap.commitAndClose()
        return self

    def setLastLogin(self):

        from datetime import datetime
        from app.constants import META_TABLE_DATEFMT

        self.lastlogin = datetime.now().strftime(META_TABLE_DATEFMT)
        self.update('lastlogin')
        return

    @classmethod
    def getUser(cls, userid):
        ##get User object using the userid
        ##has to be classmethod
        try:
            usr = User(userid)
            return usr.getSelfFromDB()
        except:
            return None
