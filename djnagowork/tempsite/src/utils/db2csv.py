#take table from db and convert it to csv

import MySQLdb as db
import pandas as pd
from pandas.io.sql import frame_query
import sys

#db2csv reads in a full table from a mysql db and puts it in a csv file
def db2csv(table, username, passwd,dbname):

    print "Connecting to ... "+dbname
    conn = db.connect("localhost",username,passwd,dbname)
    print "Connected"

    query = 'select * from '+table
    dirframe = frame_query(query, conn)
    print "Dataframe formed writing to csv"
    dirframe.to_csv('output_from_db.csv')
    print "Completed!"

    return


##sample run
if __name__ == '__main__':
    
    user = sys.argv[1]
    passwd = sys.argv[2]
    dbname = sys.argv[3]
    tabname = sys.argv[4]
    filename = tabname+'.csv'
    
    db2csv(tabname,user,passwd,dbname)
