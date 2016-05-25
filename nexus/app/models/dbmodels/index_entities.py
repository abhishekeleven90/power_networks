from app.constants import INDEX_TABLE_ENTITIES
from app.sqldb import IndexSQLDB


class Entity:

    def __init__(self, uuid, name, labels, aliases, keywords, lastmodified=None):
        self.uuid = uuid
        self.name = name
        self.labels = labels
        self.aliases = aliases
        self.keywords = keywords
        self.tablename = INDEX_TABLE_ENTITIES
        self.dbwrap = IndexSQLDB()
        self.lastmodified = lastmodified

    @classmethod
    def del_all_entities(cls):
        dbwrap = IndexSQLDB()
        dbwrap.connect()
        cursor = dbwrap.cursor()
        query = 'TRUNCATE TABLE entities'
        cursor.execute(query)
        dbwrap.commitAndClose()

    def insertEntity(self):
        self.dbwrap.connect()
        cursor = self.dbwrap.cursor()
        query = "INSERT INTO entities(uuid, name, labels, aliases, keywords) VALUES\
                ('%s','%s','%s','%s','%s')"\
                % (self.uuid, self.name, self.labels, self.aliases, self.keywords)
        print query
        numrows = cursor.execute(query)
        self.dbwrap.commitAndClose()
        return numrows

    def updateEntity(self):
        self.dbwrap.connect()
        cursor = self.dbwrap.cursor()
        query = ("UPDATE entities SET VALUES (name, labels, aliases, keywords)\
                =('%s','%s','%s','%s','%s') WHERE uuid = " + self.uuid)\
                % (self.name, self.labels, self.aliases, self.keywords)
        print query
        numrows = cursor.execute()
        self.dbwrap.commitAndClose()
        return numrows

    def getEntity(self):
        self.dbwrap.connect()
        cursor = self.dbwrap.cursor()
        query = ("SELECT * entities SET VALUES WHERE uuid = " + self.uuid)\
                % (self.name, self.labels, self.aliases, self.keywords)
        print query
        cursor.execute()
        self.dbwrap.commitAndClose()
