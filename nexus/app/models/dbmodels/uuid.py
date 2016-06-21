from app.constants import META_TABLE_UUID, META_TABLE_UUIDLAB, META_TABLE_UUIDPROPS
from app.sqldb import MetaSQLDB


class UuidTable:

    def __init__(self, uuid=None, name=''):
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_UUID
        self.uuid = uuid
        self.name = name
        return

    def create(self):

        ##TODO: can put a check here that some strings cannot be empty
        ##or in __init__


        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidTable object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (uuid, name)\
                VALUES(%d, '%s')" % (self.uuid, self.name)

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            import traceback
            traceback.print_exc()
            traceback.print_stack()
            print "[UuidTable.create: query execution error]"
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

        attr_list = ['all', 'name', 'uuid']
        assert(column in attr_list)

        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidTable] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        base_query = "UPDATE " + self.tablename + " SET "
        rest_query = " WHERE uuid= "+str(self.uuid)
        if column == "all":
            body_query = "uuid=%d, name='%s'" % (self.uuid, self.name)

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
            print "[UuidTable object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "SELECT uuid, name FROM " + self.tablename +\
                " where uuid=" + str(self.uuid)

        print query
        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) == 1)
        for r in rows:
            self.uuid = r[0]
            self.name = r[1]

        self.dbwrap.commitAndClose()
        return self

    @classmethod
    def getUuid(cls, uuid):
        uuid = UuidTable(uuid)
        return uuid.getSelfFromDB()

    def __str__(self):
        s = '[ UuidTable: uuid: ' + str(self.uuid)+' name: '\
                + str(self.name) + ']'
        return s


class UuidLabels:

    def __init__(self, changeid=None, uuid=None, label='', changetype=''):
        self.changeid = changeid
        self.uuid = uuid
        self.label = label
        self.changetype = changetype
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_UUIDLAB

        return

    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidLabels object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        query = "INSERT INTO " + self.tablename + " (changeid, uuid,\
                label, changetype) VALUES(%d, %d, '%s', %d)" %\
                (int(self.changeid), int(self.uuid), self.label, int(self.changetype))

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            import traceback
            traceback.print_exc()
            traceback.print_stack()
            print "[UuidLabels.create: query execution error]"
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
            print "[UuidLabels object] In SELECT"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        if by == 'changeid':
            bystr = " where changeid=" + str(self.changeid)
        else:
            bystr = " where uuid=" + str(self.uuid)

        rest_str = ' ORDER by changeid DESC'
        query = "SELECT changeid, uuid, label, changetype FROM "\
                + self.tablename + bystr + rest_str

        print query
        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        print len(rows)
        results_list = []
        ulabel = UuidLabels()
        for r in rows:
            ulabel.changeid = r[0]
            ulabel.uuid = r[1]
            ulabel.label = r[2]
            ulabel.changetype = r[3]
            results_list.append(ulabel.__dict__.copy())

        self.dbwrap.commitAndClose()
        for r in results_list:
            del r['tablename']
            del r['dbwrap']
        return results_list

    def getListFromDBMultiple(self, by_list=['']):

        #TODO - verify the by_list
        for by in by_list: assert(by in self.__dict__.keys())

        #TODO - connect to db
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidLabels object] In SELECT"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        #TODO - create a list of all strings 
        bystr_list = [' ' + str(by) + '=' + self.__dict__[by] for by in by_list]
            
        #TODO - join all sources by ' AND '
        bystr = ' AND '.join(bystr_list)
        #TODO - append to select query and run it as usual
        rest_str = ' ORDER by changeid DESC'
        query = "SELECT changeid, uuid, label, changetype FROM "\
                + self.tablename + " WHERE " + bystr + rest_str
        print query

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        print len(rows)
        results_list = []
        rlabel = UuidLabels()
        for r in rows:
            rlabel.changeid = r[0]
            rlabel.uuid = r[1]
            rlabel.label = r[2]
            rlabel.changetype = r[3]
            results_list.append(rlabel.__dict__.copy())

        self.dbwrap.commitAndClose()

        #TODO - return the list
        return results_list


    def __str__(self):
        s = '[ UuidLabels -- uuid: %s   label: %s  changeid: %s  changetype: %s]' %(self.uuid, self.label, self.changeid, self.changetype)
        return s

    @classmethod
    def getUuidLabelsUUId(cls, uuid):
        u = UuidLabels(uuid=uuid)
        return u.getListFromDB(by='uuid')

    @classmethod
    def getUuidLabelsChangeId(cls, changeid):
        u = UuidLabels(changeid=changeid)
        return u.getListFromDB(by='changeid')

    @classmethod
    def getUuidLabelsBothIds(cls, changeid, uuid):
        u = UuidLabels(changeid=changeid, uuid=uuid)
        return u.getListFromDBMultiple(['changeid', 'uuid'])

    #TODO - get records by uuid, label
    @classmethod
    def getUuidByLabelUuid(cls, label, uuid):
        u = UuidLabels(uuid=uuid)
        u.label = label
        return u.getListFromDBMultiple(['label', 'uuid'])


class UuidProps:

    ##TODO: see how if ' in string how to handle that!
    ##MVP '[u'naveen jindal']' will have to be handled separately
    ##IDEA: disable aliases completely in api calls?

    def __init__(self, changeid=None, uuid=None, propname='',  ##makes sense to change propname to None, this way nothing will be inserted, error!
            oldpropvalue='', newpropvalue='', changetype=''):
        import MySQLdb
        from app.utils.commonutils import Utils
        self.changeid = changeid
        self.uuid = uuid
        self.propname = propname
        self.oldpropvalue = MySQLdb.escape_string(oldpropvalue)
        self.newpropvalue = MySQLdb.escape_string(newpropvalue)
        ##TODO: add constarint in programming or db, if both none, non need of anything here
        self.changetype = changetype
        self.dbwrap = MetaSQLDB()
        self.tablename = META_TABLE_UUIDPROPS



    def create(self):
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidProps object] In create"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        ##TODO: will insert empty strings for oldpropvalue!

        query = "INSERT INTO " + self.tablename + " (changeid, uuid, propname,\
                oldpropvalue, newpropvalue, changetype) VALUES(%d, %d, '%s',\
                '%s', '%s', %d)" % (int(self.changeid), int(self.uuid), self.propname,
                self.oldpropvalue, self.newpropvalue, int(self.changetype))

        print query
        numrows = 0
        try:
            numrows = cursor.execute(query)
        except Exception as e:
            import traceback
            traceback.print_exc()
            traceback.print_stack()
            print "[UuidProps.create: query execution error]"
            self.dbwrap.commitAndClose()
        else:
            self.dbwrap.commitAndClose()

        return numrows

    def getListFromDB(self, by):

        assert (by in ['changeid', 'uuid'])
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except:
            print "[UuidProps object] In update"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        if by == "changeid":
            bystr = 'where changeid= ' + str(self.changeid)
        else: bystr = ' where uuid= ' + str(self.uuid)

        rest_str = ' ORDER by changeid DESC'
        query = "SELECT changeid, uuid, propname, oldpropvalue, newpropvalue,\
                 changetype FROM " + self.tablename + bystr + rest_str

        print query
        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        results_list = []
        uprop = UuidProps()
        for r in rows:
            uprop.changeid = r[0]
            uprop.uuid = r[1]
            uprop.propname = r[2]
            uprop.oldpropvalue = r[3]
            uprop.newpropvalue = r[4]
            uprop.changetype = r[5]
            results_list.append(uprop.__dict__.copy())

        self.dbwrap.commitAndClose()
        for r in results_list:
            del r['tablename']
            del r['dbwrap']

        return results_list

    def getListFromDBMultiple(self, by_list=['']):

        #TODO - verify the by_list
        for by in by_list: assert(by in self.__dict__.keys())

        #TODO - connect to db
        self.dbwrap.connect()
        try:
            cursor = self.dbwrap.cursor()
        except Exception as e:
            print e.message
            print "[UuidProps object] In SELECT"
            print "Cannot get cursor"
            self.dbwrap.commitAndClose()

        #TODO - create a list of all strings
        bystr_list = [' ' + str(by) + '=' + self.__dict__[by] for by in by_list]

        #TODO - join all sources by ' AND '
        bystr = ' AND '.join(bystr_list)
        #TODO - append to select query and run it as usual
        rest_str = ' ORDER by changeid DESC'
        query = "SELECT changeid, uuid, propname, oldpropvalue, newpropvalue,\
                 changetype FROM " + self.tablename + " WHERE " + bystr + rest_str
        print query

        cursor.execute(query)
        rows = cursor.fetchall()
        assert(len(rows) >= 1)
        print len(rows)
        results_list = []
        uprop = UuidProps()
        for r in rows:
            uprop.changeid = r[0]
            uprop.relid = r[1]
            uprop.propname = r[2]
            uprop.oldpropvalue = r[3]
            uprop.newpropvalue = r[4]
            uprop.changetype = r[5]
            results_list.append(uprop.__dict__.copy())

        self.dbwrap.commitAndClose()

        #TODO - return the list
        for r in results_list:
            del r['tablename']
            del r['dbwrap']

        return results_list


    def __str__(self):
        s = '[ UuidProps -- uuid: %s   propname: %s  changeid: %s  changetype: %s oldpropvalue: %s newpropvalue: %s]'
        s = s %(self.uuid, self.propname, self.changeid, self.changetype, self.oldpropvalue, self.newpropvalue)
        return s

    @classmethod
    def getUuidPropsUUId(cls, uuid):
        up = UuidProps(uuid=uuid)
        return up.getListFromDB(by='uuid')

    @classmethod
    def getUuidPropsChangeId(cls, changeid):
        up = UuidProps(changeid = changeid)
        return up.getListFromDB(by='changeid')

    @classmethod
    def getUuidPropsBothIds(cls, changeid, uuid):
        u = UuidProps(changeid=changeid, uuid=uuid)
        return u.getListFromDBMultiple(['changeid', 'uuid'])

    @classmethod
    def getUuidByPropUuid(cls, propname, propvalue, uuid):
        u = UuidProps(uuid=uuid)
        u.propname = propname
        u.newpropvalue = propvalue
        return u.getListFromDBMultiple(['uuid', 'propname', 'newpropvalue'])
