from py2neo import Graph, Node, Relationship
from py2neo.cypher import CreateNode

username = 'neo4j'
password = 'yoyo'
server = 'localhost'
port = '7474'
con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/'

graph = Graph(con_url)

#TODO: keep one connection for the entire app or multiple each time??
##Wont use this
def getGraph():
    return graph

def entity(graph, crawl_en_id):
    query = "match (n {crawl_en_id:'"+str(crawl_en_id)+"'}) return n"
    #print query
    rc = graph.cypher.execute(query)
    #print rc
    if len(rc)==0: return None
    return rc[0][0]

def relation(graph, crawl_rel_id):
    query = "match ()-[r {crawl_rel_id:'"+str(crawl_rel_id)+"'}]-() return r"
    print query
    rc = graph.cypher.execute(query)
    #print rc
    if len(rc)==0: return None
    return rc[0][0]


##Usage: print entity(graph, '5')
##Usage: print relation(graph, '6')

##to be called ONLY after safety checks
def createNodes(graph, listofnodedicts):
    print listofnodedicts
    tx = graph.cypher.begin()
    for currdict in listofnodedicts:
        props = currdict['properties']
        if not entity(graph, props['crawl_en_id']) is None:
            tx.rollback()
            return False, "Already existing entity ID, nothing pushed"
        createsome = CreateNode(*currdict['labels'],**props)
        print createsome
        tx.append(createsome)
    print tx.process()
    print tx.commit()
## createNodes(graph, [{'labels':['p','q','r'], 'properties':{'a':'b','c':'d','crawl_en_id':'399'}}])

##to be called ONLY after safety checks
def createRels(graph, listofreldicts):
    tx = graph.cypher.begin()
    for rel in listofreldicts:
        props = rel['properties']
        if not relation(graph, props['crawl_rel_id']) is None: ##it will be a redundant check as all checks are done before pushing
            tx.rollback()
            return False, "Already existing relation ID, nothing pushed"
        A = rel['start_entity'] ##will have to modify the ID to suit our needs
        B = rel['end_entity'] ##will have to modify the ID to suit our needs
        C = rel['label']
        D = '{ '
        for key in rel['properties']:
            D = D + key + ' : \''+rel['properties'][key]+ '\', '
        D = D[:-2] + ' }' 
        print D
        statement = 'MATCH (a {crawl_en_id:\'%s\'}), (b {crawl_en_id:\'%s\'}) CREATE (a)-[rtt:%s %s]->(b) return rtt' %(A,B,C,D)
        print statement
        print tx.append(statement)
    print tx.process()
    print tx.commit()
##Usage:
# #createRels(graph, [{
#             "end_entity": "2",
#             "label": "worksIn",
#             "properties":
#             {
#                 "bidirectional": "no",
#                 "crawl_rel_id": "rel_NexusToken1_njconn1_1",
#                 "startdate": "01/01/2010"
#             },
#             "start_entity": "3"
#         }])


## we can take a list of nodedicts and a list of rel dicts
## see that node dicts ids not exist already
## see that rel dicts ids not exist already
## see that start id and end id already in graph db or in the node dict provided
## only after this is the post/push safe --> can be done
##TODO: remove token and taskname when not needed
def isSafePost(graph, listOfNodeDicts, listOfRelDicts, token, taskname):
    
    print '##'
    print listOfRelDicts
    print '##'
    print listOfNodeDicts
    print '##'
    
    print 'Analysing entity ids!'
    from sets import Set
    currnodekeys = Set()
    for nodedict in listOfNodeDicts:
        ##check if this exist in graphdb
        if not entity(graph, nodedict['properties']['crawl_en_id']) is None:
            return False, 'Entity ID: ' + str(nodedict['properties']['crawl_en_id']) + ' already exists in crawl db'
        currnodekeys.add(str(nodedict['properties']['crawl_en_id']))
        
    print currnodekeys
        
    print 'Analysing relation ids!'
    for reldict in listOfRelDicts:
        
        ##check if this exist in graph db
        if not relation(graph, reldict['properties']['crawl_rel_id']) is None:
            return False, 'Relation ID: ' + str(reldict['properties']['crawl_rel_id']) + ' already exists in crawl db'
        
        ##also check start id in nodedict and graphdb
        print '-------'
        print reldict['start_entity']
        print reldict['start_entity'] in currnodekeys
        print (entity(graph,reldict['start_entity']) is None)
        if (not str(reldict['start_entity']) in currnodekeys) and (entity(graph,str(reldict['start_entity'])) is None):
            return False, 'Relation ID: ' + str(reldict['properties']['crawl_rel_id']) + ' has a reference to non-existent Entity ID '+str(reldict['start_entity'])
        
        ##also check end id in nodedict and graphdb
        if (not str(reldict['end_entity']) in currnodekeys) and (entity(graph,str(reldict['end_entity'])) is None):
            return False, 'Relation ID: ' + str(reldict['properties']['crawl_rel_id']) + ' has a reference to non-existent Entity ID '+str(reldict['end_entity'])
        print reldict['properties']['crawl_rel_id']
    return True, "Success"


def testIsSafePost(graph):
    nodeslist = []
    relslist = []
    startnodeid = 7
    startrelid = 200
    numnodes = 3
    
    for i in range(numnodes):
        currnode = {}
        currnode['labels'] = ['abcd','xyz']
        currprops = {}
        currprops['name'] = 'name ' + str(startnodeid + i)
        currprops['crawl_en_id'] = str(startnodeid + i)
        currnode['properties'] = currprops
        nodeslist.append(currnode)
    #print nodeslist
    
    for i in range(numnodes+1):
        currrel = {}
        startid = startnodeid + i
        endid = startid + 1
        if endid >= (startnodeid + numnodes):
            endid = startnodeid
        currrel['start_entity'] = startid
        currrel['end_entity'] = endid
        currrel['label'] = 'relationlabel'
        currprops = {}
        currprops['startdate'] = '01/01/2000'
        currprops['enddate'] = '10/10/2014'
        currprops['crawl_rel_id'] = startrelid + i
        currrel['properties'] = currprops
        relslist.append(currrel)
    #print relslist
    
    return nodeslist, relslist
    
##Usage: nl, rl = testIsSafePost(graph)
##Usage: isSafePost(graph, nl, rl, '', '')


def postSubGraph(graph, nodes, links, token, taskname):
    
    ##make a list of nodes
    ##make a list of links
    ##check for isSafePost
    ##then createNodes
    ##then create Rels

    nodeList = []
    for node in nodes:
        nodeList.append(nodes[node])
    
    linkList = []
    for link in links:
        linkList.append(links[link])

    safe, msg = isSafePost(graph, nodeList, linkList, token, taskname)
    
    if not safe:
        return safe, msg

    createNodes(graph, nodeList) ##MAJOR TODO: "includeStats": True???
    createRels(graph, linkList)

    return True, "Success"