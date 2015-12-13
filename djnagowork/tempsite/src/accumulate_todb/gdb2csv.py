import pandas as pd
from py2neo import Graph,Node
import pkg_resources as pr
import sys
import csv2graphdb as cdb

print "[main] - connecting to db..."
g = cdb.connectdb()

print "[main] - now getting df"
df = cdb.get_entities_graphdb(g,"Party","Party","AAP")
print df
print "[main] - COMPLETED"
df.to_csv("neo4j_result.csv")


