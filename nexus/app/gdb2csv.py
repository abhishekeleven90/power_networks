import pandas as pd
from py2neo import Graph,Node
import pkg_resources as pr
import sys
import csv2gdb as cdb
import search_query as sq
def get_gdb_entity(query):
    print "[get_gdb_entity] - connecting to db..."
    g = cdb.connectdb()

    print "[get_gdb_entity] - now getting df"
    df = cdb.get_entities_graphdb(g,"Party",prop="Party",prop_val=query)
    #df = cdb.get_entities_graphdb(g,"Party")#for now party is the only label . TODO - Party Politician
    #print df
    #df2 = sq.search_query(df,query)
    print "[get_gdb_entity] - COMPLETED"
    return df
    #return df2


if __name__ == "__main__":
    print "[main] - connecting to db..."
    g = cdb.connectdb()

    print "[main] - now getting df"
    df = cdb.get_entities_graphdb(g,label="Party",property_key="Party",property_value="AAP")
    print df
    print "[main] - COMPLETED"
    df.to_csv("neo4j_result.csv")
