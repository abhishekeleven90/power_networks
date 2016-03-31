"""
Module - gdb2csv.py

It imports entity and relationships from the graph db
using csv2gdb.py.
Put appropriates similarity measure in the query and df to get results.
Returns df containing filtered results matched by jaro winkler distance
Uses - 
-----------
csv2gdb.py for reading in the graphdb
search_query.py to match similarity measure between query and df and filter out data

"""

import pandas as pd
from py2neo import Graph,Node
import pkg_resources as pr
import sys
import csv2gdb as cdb
import search_query as sq
import threading

class gcd(threading.Thread):

    thrd_list = []
    df_list = []
    tab_list =[]
    g = cdb.connectdb()
    listLock = threading.Lock()

    def __init__(self,query):
        threading.Thread.__init__(self)
        self.query = query
        self.lab ='Party' 
        self.thres = 0.6

    def __init__(self,query,lab,thres):
        threading.Thread.__init__(self)
        self.query = query
        self.lab = lab
        self.thres = thres

    def run(self):

        print "[get_gdb_entity] - now getting df"
        df = cdb.get_entities_graphdb(gcd.g,self.lab)#for now party is the only label . TODO - Politicians
        df2 = sq.search_query(df=df,query=self.query,thres = self.thres)
        print "[get_gdb_entity] - COMPLETED"
        #return df
        #return df2
        if not df2.empty:
            #print "[get_gdb_entity] - label -{}. acquire locks".format(self.lab)
            #gcd.listLock.acquire()
            gcd.df_list.append(df2.to_html(classes = "table"))
            gcd.tab_list.append(self.lab)
            #print "[get_gdb_entity] - label -{}. release locks".format(self.lab)
            #gcd.listLock.release()



#given a list of labels we get a list of tables matching them
def get_gdb_entity(query,lab_list,thres_list):

    gcd.thrd_list = []
    gcd.df_list = []
    gcd.tab_list = []
    for lab,thres in zip(lab_list,thres_list):
        pf = gcd(query,lab,thres)
        gcd.thrd_list.append(pf)
        pf.start()
    for thrds in gcd.thrd_list: thrds.join()

    return (gcd.df_list,gcd.tab_list)


#simply get an entity with given label and props
def get_gdb_entity_simple(label,propdic=None):

    prop_key,prop_val= None,None
    if propdic :
        prop_key =propdic.keys()[0]
        prop_val = propdic.values()[0]

    g = cdb.connectdb()
    df = cdb.get_entities_graphdb(g,label,prop_key,prop_val)
    return df

#simply get a relationship with given name
def get_gdb_rel_simple(label,propdic = None):

    prop_key,prop_val = None,None
    if propdic:
        prop_key = propdic.keys()[0]
        prop_val = propdic.values()[0]

    g = cdb.connectdb()
    df = cdb.get_rel_graphdb(g,label,prop_key,prop_val)
    return df
#TODO - get_gdb_relationships

if __name__ == "__main__":
    print "[main] - connecting to db..."
    g = cdb.connectdb()

    print "[main] - now getting df"
    df = cdb.get_entities_graphdb(g,label="Party",property_key="Party",property_value="AAP")
    print df
    print "[main] - COMPLETED"
    df.to_csv("neo4j_result.csv")
