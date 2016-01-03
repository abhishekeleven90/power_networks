"""
Module - csv2graphdb

Contains functions to read the graphdb
and put csv file data to graphdb.
Basic read/write module.

Uses
-----------
py2neo lib

functions
-------------
function connectdb
Returns a graph instance

function load_entities_csv
filename - csv file's absolute path
labels - label to give in nodes
prop_list - properties to give to nodes
Returns None

"""

import pandas as pd
from py2neo import Graph,Node,Relationship
import pkg_resources as pr
import sys
username = 'neo4j'
password = 'yoyo'
server = 'localhost'
port = '7474'
con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/'

def connectdb():
#return a graph by con_url
    secure_graph = Graph(con_url)
    return secure_graph


#get all relationships of a particular label from the graph db

def get_rel_graphdb(g,rel_type,prop_key = None,prop_val=None):

    df_list = []
    i = 0
    print "[get_rel_graphdb] -Scanning all relationship from graph ... of given label - {}".format(rel_type)

    rels = g.match(rel_type=rel_type)
    for r in rels:

        print "[get_rel_graphdb] - relationship no- "+str(i)
        cols1 = r.end_node.properties.keys()
        print cols1
        print r.end_node.properties

        cols2 = r.start_node.properties.keys()
        print cols2
        print r.start_node.properties

        cols = cols1+cols2
        props = dict(r.start_node.properties)
        props['relationship'] = rel_type
        props.update(r.end_node.properties)

        tmp_df = pd.DataFrame(columns = props.keys()) 
        tmp_df.loc[0] = pd.Series(props)
        df_list.append(tmp_df)
        i += 1

    if df_list:
        df = pd.concat(df_list, ignore_index = True)
    return df

#get all entities from the graph db
def get_entities_graphdb(g,label,prop = None, prop_val = None):

    df_list = []
    i = 0
    print "[get_entities_graphdb] -Scanning all entities from graph ..."
    print "prop -{}".format(prop)
    print "prop_val -{}".format(prop_val)
    for node in g.find(label = label,property_key =prop, property_value = prop_val ):

        print "[get_entities_graphdb] - node - "+str(i)
        cols = node.properties.keys()
        #print cols
        #print node.properties

        tmp_df = pd.DataFrame(columns = cols)
        tmp_df.loc[0] = pd.Series(node.properties)
        df_list.append(tmp_df)
        i += 1

    if df_list:
        df = pd.concat(df_list, ignore_index = True)
    else: df = pd.DataFrame()
    return df

#load entities from csv and create nodes in graph
def load_entities_csv(g,filename, label,prop_list):

    #Note prop_list must contain respective column names from the dataset
    df = pd.read_csv(filename)

    print "[load_entities_csv] - df -->all columns to strings"
    for i in df.columns:
        df[i] = df[i].astype(str)

    print "[load_entities_csv] - df given:-"
    print df

    for i,r in df.iterrows():
        print '[load_entities_csv] - scanning row -  {}'.format(i)
        nd = Node()
        nd.labels.add(label)
        for c in prop_list:
            nd.properties[c] = r[c]
        
        print '[load_entities_csv] - creating node...'
        g.create(nd)
        print '[load_entities_csv] - node successfully created'

    return


#similarly we load relationships from csv
#it assumes a particular format for csvs
#first two columns - label1,label2 property(say name). next two columns - relationship property.
def load_relationships_csv(g,filename,label1,label2,rel_name):

    df = pd.read_csv(filename)
    pkey1,pkey2,rprop = df.columns[0],df.columns[1],df.columns[2]
    for i,r in df.iterrows():
        nd1 = g.find(label1,property_key = pkey1,property_value = r[pkey1])
        nd2 = g.find(label2,property_key = pkey2,property_value = r[pkey2])
        rel = Relationship(nd1,nd2,rel_name)
        rel.properties[rprop] = r[rprop]
        g.create(rel)
    return


#naive function to get a relationship from label1 to label2 with name rel_name
def load_relationships(g,label1,label2,rel_name):

    i= 0
    for node1 in g.find(label = label1):
        for node2 in g.find(label = label2):
            rel = Relationship(node1,rel_name,node2)
            g.create(rel)
            print "[load_relationships]- rel no.-{} created.".format(i)
            i += 1
    return


#script to enter data to graphdb using cli
#input file assumed to be in src/input folder
if __name__ =='__main__':

    print "[main] - connecting to db..."
    g = connectdb()

    #Amartya - 2 Jan changed to test
    #to load entities in graphdb
    #if len(sys.argv) < 4:
    #    print "Usage: python csv2db.py filename label properties"
    #    exit(2)
    #filename = sys.argv[1]
    #filename = pr.resource_filename('src.input',filename)
    #label = sys.argv[2]
    #prop_list = []
    #for i in xrange(3,len(sys.argv)):
    #    prop_list.append(sys.argv[i])

    #print "[main]- prop list"
    #print prop_list
    #print "[main]- loading entities to gdb"
    #load_entities_csv(g,filename,label,prop_list)
    ## Amartya - 2 Jan changed to test

    #to load relationships
    if len(sys.argv) < 4:
        print "Usage: python csv2gdb.py label1 label2 rel_name"
        exit(3)
    lab1 = sys.argv[1]
    lab2 = sys.argv[2]
    rel_name = sys.argv[3]
    load_relationships(g,lab1,lab2,rel_name)

    ## Amartya - 2 Jan changed to test
    #print "[main] - now getting df"
    #df = get_entities_graphdb(g,label = 'Party',prop = 'partyid',prop_val = 2)
    #print df
    ## Amartya - 2 Jan changed to test
    print "[main] - COMPLETED"

