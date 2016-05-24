from app.constants import META_TABLE_UUID
import MySQLdb as mysqldb
from app.sqldb import MetaSQLDB

class UUIDTable:

    def __init__(self, name):
        self.tablename  = META_TABLE_UUID
        pass