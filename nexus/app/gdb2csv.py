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
import gc

def get_gdb_entity(query,lab = "Party",thres = 0.6):
    print "[get_gdb_entity] - connecting to db..."
    g = cdb.connectdb()

    print "[get_gdb_entity] - now getting df"
    df = cdb.get_entities_graphdb(g,lab)#for now party is the only label . TODO - Politicians
    print df
    df2 = sq.search_query(df=df,query=query,thres = thres)
    print "[get_gdb_entity] - COMPLETED"
    #return df
    return df2

#TODO - get_gdb_relationships

if __name__ == "__main__":
    print "[main] - connecting to db..."
    g = cdb.connectdb()

    print "[main] - now getting df"
    df = cdb.get_entities_graphdb(g,label="Party",property_key="Party",property_value="AAP")
    print df
    print "[main] - COMPLETED"
    df.to_csv("neo4j_result.csv")
