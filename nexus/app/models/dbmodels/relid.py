from app.constants import META_TABLE_RELID, META_TABLE_RELIDLAB, META_TABLE_RELIDPROPS
from app.sqldb import MetaSQLDB


class RelIdTable:

    def __init__(self, relid, reltype='', startuuid=None, enduuid=None):
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_RELID
        self.relid = relid
        self.reltype = reltype
        self.startuuid = startuuid
        self.enduuid = enduuid
        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[RelIdTable object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (relid, reltype, startuuid,\
                enduuid) VALUES(%d, '%s', %d, %d)" % (self.relid,
                self.reltype, self.startuuid, self.enduuid)

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

    def delete(self):
        ##delete self object into db
        ##TODO - later
        pass

    ##Update reltable.,   Not present
    ##For the RelLabels and RelProps class
    def update(self, column='all'):
        ##update self object into db

        attr_list = ['all', 'reltype', 'startuuid', 'enduuid']
        assert(column in attr_list)

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[RelIdTable] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        base_query = "UPDATE " + self.tablename + " SET "
        rest_query = " WHERE relid= "+str(self.relid)
        if column == "all":
            body_query = "reltype='%s', startuuid=%d, enduuid = %d" % \
                    (self.reltype, self.startuuid, self.enduuid)

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
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            print e.message
            self.dbwrap.commitAndClose()
            exit(3)
        else:
            self.dbwrap.commitAndClose()

        return numrows

    def getSelfFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[User object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT relid, reltype, startuuid, enduuid \
                 FROM " + self.tablename + " where relid=" + str(self.relid)

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.relid = r[0]
            self.reltype = r[1]
            self.startuuid = r[2]
            self.enduuid = r[3]

        self.dbwrap.commitAndClose()
        return self

    @classmethod
    def getRel(cls, relid):
        rel = RelIdTable(relid)
        return rel.getSelfFromDB()

    def __str__(self):
        print '[ Relation: relid: '+str(self.relid)+' startuuid: '\
                + str(self.startuuid)+' enduuid: '+str(self.enduuid)+' ]'
        return


class RelLabels:

    def __init__(self, changeid=None, relid=None, label='', changetype=None):
        self.changeid = changeid
        self.relid = relid
        self.label = label
        self.changetype = changetype
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_RELIDLAB

        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[Taskusers object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (changeid, relid,\
                label, changetype) VALUES(%d, %d, '%s', %d)" %\
                (self.changeid, self.relid, self.label, self.changetype)

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
        except Exception as e:
            print e.message
            print "[RelLabels object] In SELECT"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        #if by == 'changeid':
        #    bystr = "changeid='" + self.userid + "'"
        #else:
        #    bystr = "taskid=" + self.taskid

        query = "SELECT changeid, relid, label, changetype FROM "\
                + self.tablename + " where changeid=" + str(self.changeid)

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        print len(rows)
        results_list = []
        rlabel = RelLabels()
        for r in rows:
            rlabel.changeid = r[0]
            rlabel.relid = r[1]
            rlabel.label = r[2]
            rlabel.changetype = r[3]
            results_list.append(rlabel.__dict__.copy())

        self.dbwrap.commitAndClose()
        return results_list

    @classmethod
    def getRelLabels(cls, changeid):
        r = RelLabels(changeid=changeid)
        return r.getListFromDB(changeid)


class RelProps:

    def __init__(self, changeid=None, relid=None, propname='',
            oldpropvalue='', newpropvalue='', changetype=None):
        self.changeid = changeid
        self.relid = relid
        self.propname = propname
        self.oldpropvalue = oldpropvalue
        self.newpropvalue = newpropvalue
        self.changetype = changetype
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_RELIDPROPS
        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[RelProps object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (changeid, relid, propname,\
                oldpropvalue, newpropvalue, changetype) VALUES(%d, %d, '%s',\
                '%s', '%s', %d)" % (self.changeid, self.relid, self.propname,
                self.oldpropvalue, self.newpropvalue, self.changetype)

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            print "query execution error"
            self.dbwrap.commitAndClose()
        else:
            self.dbwrap.commitAndClose()

        return numrows

    def getListFromDB(self):

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[RelProps object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT changeid, relid, propname, oldpropvalue, newpropvalue,\
                 changetype FROM " + self.tablename + " where changeid=" + \
                 str(self.changeid)

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        results_list = []
        rprops = RelProps()
        for r in rows:
            rprops.changeid = r[0]
            rprops.relid = r[1]
            rprops.propname = r[2]
            rprops.oldpropvalue = r[3]
            rprops.newpropvalue = r[4]
            rprops.changetype = r[5]

            results_list.append(rprops.__dict__.copy())

        self.dbwrap.commitAndClose()
        return results_list

    @classmethod
    def getRelProps(cls, changeid):
        rp = RelProps(changeid)
        return rp.getListFromDB()

