from app.constants import META_TABLE_TASKS, META_TABLE_TASKUSERS, META_TABLE_TASKLOG
from app.sqldb import MetaSQLDB
from datetime import datetime


class Tasks:

    def __init__(self, ownerid = None, name=None, description='description', iscrawled=0):
        self.ownerid = ownerid
        self.name = name
        self.taskid = None
        self.description = description
        self.iscrawled = iscrawled
        self.createdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_TASKS
        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Tasks object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (ownerid, name, description,\
                createdate, iscrawled) VALUES('%s', '%s', '%s', '%s', %d)" % (self.ownerid,
                self.name, self.description, self.createdate, self.iscrawled)

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            print e.message
            print "query execution error"
            self.dbwrap.commitAndClose()

        else:
            self.taskid = cursor.lastrowid
            self.dbwrap.commitAndClose()
        return numrows

    def delete(self):
        ##delete self object into db
        ##TODO - later
        pass

    def update(self, column='all'):
        ##update self object into db

        attr_list = ['all', 'name', 'description']
        assert(column in attr_list)

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Tasks object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        base_query = "UPDATE " + self.tablename + " SET "
        rest_query = " WHERE taskid= "+str(self.taskid)
        if column == "all":
            body_query = "name='%s', description='%s'" % \
                    (self.name, self.description)
            query = base_query + body_query + rest_query
            print "UPDATE query"
            print query

        else:
            t = type(column)
            val = getattr(self, column)
            if t == int:
                typestr = "%d"
            else: typestr = "'%s'"
            body_query = (column+"="+typestr) % (val)
            query = base_query + body_query + rest_query
            print "UPDATE query"
            print query

        numrows = 0
        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose()

        return numrows

    def getSelfFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT ownerid, taskid, name, description, iscrawled, createdate \
                 FROM " + self.tablename + " where taskid=" + str(self.taskid)

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.ownerid = r[0]
            self.taskid = r[1]
            self.name = r[2]
            self.description = r[3]
            self.iscrawled = r[4]
            self.createdate = r[5]

        self.dbwrap.commitAndClose()
        return self

    @classmethod
    def getTask(cls, taskid):
        tsk = Tasks()
        tsk.taskid = taskid
        return tsk.getSelfFromDB()
        
    def __str__(self):
        print '[ Task: taskid: '+str(self.taskid)+' name: '\
                + str(self.name)+' descr: '+str(self.description)+' ]'
        return


class Taskusers:

    def __init__(self, taskid=None, userid=''):
        self.taskid = taskid
        self.userid = userid
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_TASKUSERS
        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Taskusers object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (taskid, userid)\
                VALUES(%d, '%s')" % (self.taskid, self.userid)

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            print e.message
            print "query execution error"
            self.dbwrap.commitAndClose()
        else:
            self.dbwrap.commitAndClose()
        return numrows

    def getListFromDB(self, by):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Taskusers object] In SELECT"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        if by == 'userid':
            bystr = "userid='" + self.userid + "'"
        else:
            bystr = "taskid=" + str(self.taskid)

        query = "SELECT userid, taskid FROM " + self.tablename + \
                " WHERE " + bystr

        cursor.execute(query)
        rows = cursor.fetchall()
        #assert(len(rows) == 1)
        result_list = []
        for r in rows:
            self.userid = r[0]
            self.taskid = r[1]
            if by == 'userid':
                result_list.append(self.taskid)
            else:
                result_list.append(self.userid)


        self.dbwrap.commitAndClose()
        return result_list


class Tasklog:

    def __init__(self, taskid=None, userid='', description='', jsondump=''):
        self.taskid = taskid
        self.userid = userid
        self.description = description
        self.jsondump = jsondump
        self.dumpdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_TASKLOG
        return
    

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Tasklog object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (taskid, userid,\
                description, jsondump, dumpdate) VALUES(%d, '%s', '%s', '%s', '%s')" % \
                (self.taskid, self.userid, self.description, self.jsondump, self.dumpdate)

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            print e.message
            print "query execution error"

            self.dbwrap.commitAndClose()
        else:
            self.dbwrap.commitAndClose()

        return numrows

    def getSelfFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[Tasklog object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT userid, taskid, description, jsondump, dumpdate \
                 FROM " + self.tablename + " where taskid=" + str(self.taskid) + \
                 " AND userid='" + self.userid + "'"

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.userid = r[0]
            self.taskid = r[1]
            self.description = r[2]
            self.jsondump = r[3]
            self.dumpdate = r[4]

        self.dbwrap.commitAndClose()
        return self

    @classmethod
    def getTasklog(cls, userid, taskid):
        tl = Tasklog(taskid, userid)
        return tl.getSelfFromDB()


