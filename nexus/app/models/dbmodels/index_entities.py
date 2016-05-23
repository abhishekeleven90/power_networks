from app.constants import INDEX_TABLE_ENTITIES
from app.sqldb import IndexSQLDB

class Entity:

    def __init__(self, uuid, name, aliases, keywords):
        self.uuid = uuid
        self.name = name
        self.aliases = aliases
        self.keywords = keywords
        self.tablename = INDEX_TABLE_ENTITIES
        self.dbwrap = IndexSQLDB()

    def del_all_index(self):
        self.dbwrap.connect()
        cursor = self.dbwrap.cursor()
        query = 'TRUNCATE TABLE entities'
        cursor.execute(query)
        self.dbwrap.closeAndCommit()







