# #META TABLE CONNECT CONFIG
# META_SQL_DBNAME = 'nexus'
# META_SQL_DBHOST = '10.237.27.151'
# META_SQL_DBUSER = 'nexususer'
# META_SQL_DBPASSWORD = 'yoyo'
# META_SQL_DBPORT = 3306

# #INDEX TABLE CONNECT CONFIG
# INDEX_SQL_DBNAME = 'power_nexus'
# INDEX_SQL_DBHOST = '10.237.27.67'
# INDEX_SQL_DBUSER = 'nexus'
# INDEX_SQL_DBPASSWORD = 'yoyo'
# INDEX_SQL_DBPORT = 3306

#META TABLE CONNECT CONFIG
META_SQL_DBNAME = 'nexus'
META_SQL_DBHOST = 'localhost'
META_SQL_DBUSER = 'root' ##nexususer
META_SQL_DBPASSWORD = 'yoyo'
META_SQL_DBPORT = 3306

#INDEX TABLE CONNECT CONFIG
INDEX_SQL_DBNAME = 'power_nexus'
INDEX_SQL_DBHOST = 'localhost'
INDEX_SQL_DBUSER = 'root'
INDEX_SQL_DBPASSWORD = 'yoyo'
INDEX_SQL_DBPORT = 3306

#CORE_GRAPH_CONNECT CONFIG
CORE_GRAPH_HOST = 'localhost'
CORE_GRAPH_USER = 'neo4j'
CORE_GRAPH_PORT = '7474'  #fot http this is
CORE_GRAPH_PASSWORD = 'yoyo'

#AUTHORIZATION FOR CORE GRAPH
#OBTAINED FROM POSTMAN REQUEST
AUTHORIZATION_HASH = 'Basic bmVvNGo6eW95bw=='

##CRAWl_DB VARIABLES
CRAWL_GRAPH_HOST = 'localhost'
CRAWL_GRAPH_USER = 'neo4j'
CRAWL_GRAPH_PORT = '8484' ##for http this is
CRAWL_GRAPH_PASSWORD = 'yoyo'
CRAWL_LOCK_LIMIT = 60 ##seconds
CRAWl_JOB_INTERVAL = 10 ##seocnds

#CORE_GRAPH_SYMBOLS
CORE_GRAPH_UUID = 'uuid'
CORE_GRAPH_RELID = 'relid'
CORE_GRAPH_HENID = 'henid'

#CRAWL GRAPH SYMBOLS
CRAWL_EN_ID_NAME = '_crawl_en_id_'
CRAWL_REL_ID_NAME = '_crawl_rel_id_'
CRAWL_HEN_ID_NAME = '_crawl_en_id_' ##TODO: for now will have to change to give this some good id, but will have to change in api too.
RESOLVEDWITHUUID = '_resolvedWithUUID_'
RESOLVEDWITHRELID = '_resolvedWithRELID_'
RESOLVEDWITHHENID = '_resolvedWithHENID_'
CRAWL_VERIFIEDBY = '_verifiedby_'
CRAWL_LOCKEDBY = '_lockedby_'
CRAWL_LOCKEDAT = '_lockedat_'
CRAWL_PUSHEDBY = '_pushedby_'
CRAWL_VERIFYDATE = '_verifydate_'
CRAWL_PUSHDATE = '_pushdate_'
CRAWL_FETCHDATE = '_fetchdate_'
CRAWL_SOURCEURL = '_sourceurl_'
CRAWL_TASKID = '_taskid_'
CRAWL_TASKTYPE = '_tasktype_'
CRAWL_NODENUMBER = '_nodenumber_'
CRAWL_RELNUMBER = '_relnumber_'
CRAWL_EN_ID_FORMAT = "en_%s_%s"
CRAWL_REL_ID_FORMAT = "rel_%s_%s"
LABEL_HYPEREDGE_NODE = 'hyperedgenode'
LABEL_ENTITY = 'entity'
CORE_VALIDATED_PROPS = ["startdate","enddate","bidirectional","iscurrent"]



#SOLR CONFIG
SOLR_HOST = 'localhost'
SOLR_PORT = 8983
SOLR_CORE = 'mtp2'

##META TABLE NAMES
META_TABLE_USER = 'users'
META_TABLE_UUID = 'uuidtable'
META_TABLE_RELID = 'relidtable'
META_TABLE_HENID = 'henidtable'
META_TABLE_TASKS = 'tasks'
META_TABLE_TASKUSERS = 'taskusers'
META_TABLE_TASKLOG = 'tasklog'
META_TABLE_CHANGE = 'changetable'
META_TABLE_RELIDPROPS = 'relidprops'
META_TABLE_RELIDLAB = 'relidlabels'
META_TABLE_UUIDLAB = 'uuidlabels'
META_TABLE_UUIDPROPS = 'uuidprops'
META_TABLE_DATEFMT = '%Y-%m-%d %H:%M:%S'

##INDEX TABLE NAMES
INDEX_TABLE_ENTITIES = 'entities'

##MULTI-VALUED PROP
##contains for both nodes and rels overall
MVPLIST = ["aliases","phone","address","email"]
##TODO: add to api validation

##GOOGLE MAPS API KEY
APIKEY="AIzaSyALThUkSSrl0qMGPnaewBghOhkA81vDQHk"

##ROLES
ROLE_USER = 1
ROLE_CRAWLER = 2
ROLE_VERIFIER = 3
ROLE_MODERATOR = 5
ROLE_ADMIN = 7

##DATE FORMAT
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

##CHANGETYPE
CHANGE_INSERT = 1
CHANGE_DELETE = 0
CHANGE_MODIFY = 2

##SESSION VARIABLES
SESSION_KIND = 'kind'
SESSION_TASKTYPE_NAME = 'tasktype'
SESSION_CRAWL_VAL = 'crawl'
SESSION_WIKI_VAL = 'wiki'
