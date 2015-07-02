"""
Module - csv2graphdb

function connectdb
Returns a graph instance

function load_entities_csv
filename - csv file's absolute path
labels - label to give in nodes
prop_list - properties to give to nodes

Returns None
"""

import pandas as pd
from py2neo import Graph,Node
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


#get all entities from the graph db

def get_entities_graphdb(g,label):

    df_list = []
    i = 0
    print "Scanning all entities from graph ..."
    for node in g.find(label = label):

        print "node - "+str(i)
        cols = node.properties.keys()
        print cols
        print node.properties

        tmp_df = pd.DataFrame(columns = cols)
        tmp_df.loc[0] = pd.Series(node.properties)
        df_list.append(tmp_df)
        i += 1

    df = pd.concat(df_list, ignore_index = True)
    return df


#load entities from db and create nodes in graph
def load_entities_csv(g,filename, label,prop_list):

    #Note prop_list must contain respective column names from the dataset
    df = pd.read_csv(filename)
    print "df given:-"
    print df

    for i,r in df.iterrows():
        print 'scanning row -  {}'.format(i)
        nd = Node()
        nd.labels.add(label)
        for c in prop_list:
            nd.properties[c] = r[c]
        
        print 'creating node...'
        g.create(nd)
        print 'node successfully created'

    return

#similarly we load relationships from csv
#def load_relationships(filename, )

#run the main function
if __name__ =='__main__':

    print "connecting to db..."
    g = connectdb()
    filename = sys.argv[1]
    filename = pr.resource_filename('src.input',sys.argv[1])
    print "loading entities to db"
    load_entities_csv(g,filename,"Party",['Party','partyid'])

    print "now getting df"
    df = get_entities_graphdb(g,"Party")
    print df
    print "COMPLETED"


