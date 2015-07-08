###
#   To setup the system:
## create (n:version_cp:system {next:'1'}),   (p:node_id:system {next:'1'}),  (q:rel_id:system {next:'1'})
##

##first delete all the nodes and rels that are in the db
##or change the db for better

from py2neo import Graph, Node, Relationship
username = 'neo4j'
password = 'yoyo'
server = 'localhost'
port = '7474'
con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/'

def getGraph():
    return Graph(con_url)

##helper function to help delete all junk created in graph
## use only during development
def delete_all(graph):
    graph.delete_all()
    
##this is how we use the intenal ids of the graph
##should we use it?? most people say no
## anyways, made the method for future use
## Use : getNodeByInternalId(graph, 152)
def getNodeByInternalId(graph,id):
    a  = graph.node(id) #getting by id given internally by neo4j
    a.pull()
    return a

## similar to above
## Use : getRelByInternalId(graph, 4) 
def getRelByInternalId(graph,id):
    a  = graph.relationship(id) 
    a.pull()
    return a

##returns Relation which has custom id in 'ids' as we have given it
## but the relation should be latest, that is cp_end should be infinity, otherwise throws an error
#Use:
#rc = getLatestRelById(graph, '4') ##IndexError if not latest!! TODO
#print isinstance(rc,Relationship)
#rc
def getLatestRelById(graph,ids):
    query = "match ()-[r {relid:'"+ids+"',cp_end:'Infinity'}]-() return r"
    #print query
    rc = graph.cypher.execute("match ()-[r {relid:'"+ids+"',cp_end:'Infinity'}]-() return r")
    #print len(rc)
    #print rc
    return rc[0][0]

##Use: id used is what we have given by ourselves
##n1 = getLatestNodeById(graph, '1') # ##IndexError if not latest!! TODO
#print isinstance(n1,Node)
#n1
def getLatestNodeById(graph,ids):
    print '' + str(ids)
    rc = graph.cypher.execute("match (n {nodeid:'"+ids+"',cp_end:'Infinity'}) return n")
    return rc[0][0]

##Use: getLastCheckPoint(graph)
## returns a string telling which was the last checkpoint in the graph
def getLastCheckPoint(graph): #returns a string
    a=graph.find_one('version_cp')
    return str(int(a.properties['next'])-1)

##Use: getNextCheckPoint(graph)
##returns a string telling which will be the next checkpoint in the graph
def getNextCheckPoint(graph): ##returns a string
    a=graph.find_one('version_cp')
    return a.properties['next']

##Use: getNextNodeId(graph)
#returns node id for next node if any is created
def getNextNodeId(graph):
    a=graph.find_one('node_id')
    return a.properties['next']

##Use: getNextRelId(graph)
#returns rel id for next rel if any is created
def getNextRelId(graph):
    a=graph.find_one('rel_id')
    return a.properties['next']

#Use: incrementCheckPoint(graph)
#to be used whwn an update has been done
def incrementCheckPoint(graph):
    a=graph.find_one('version_cp')
    a.properties['next'] = str(int(a.properties['next'])+1)
    a.push()
    return a

#Use: incrementNodeId(graph)
#to be used when a node with previous id has been created just now
def incrementNodeId(graph):
    a=graph.find_one('node_id')
    a.properties['next'] = str(int(a.properties['next'])+1)
    a.push()
    return a

#Use: incrementRelId(graph)
#to be used when a node with previous id has been created just now
def incrementRelId(graph):
    a=graph.find_one('rel_id')
    a.properties['next'] = str(int(a.properties['next'])+1)
    a.push()
    return a

#Use: create_with_cp(graph,node1,node2,rel2,rel2)
##alternative to graph.create(entities)
def create_with_cp(graph,*entities):
    cp=getNextCheckPoint(graph)
    stmt = create_with_cp_helper(graph,cp,entities)
    incrementCheckPoint(graph)
    return stmt

#Use: This method creates the entities with the checkpoint given in cp variable
#TODO: copied from core.py, make it easy
def create_with_cp_helper(graph,cp,*entities):
    from py2neo.cypher.create import CreateStatement
    statement = CreateStatement(graph)
    #print entities
    for entity in entities[0]: #to handle the tuple problem
        entity["cp_start"]=cp
        entity["cp_end"]="Infinity"
        if(isinstance(entity,Node)): ##TODO: afterwards, reduce database hits somehow
            ids=getNextNodeId(graph)
            entity["nodeid"]=ids
            incrementNodeId(graph)
        elif(isinstance(entity,Relationship)):
            ids=getNextRelId(graph)
            entity["relid"]=ids
            incrementRelId(graph)
        statement.create(entity)
    return statement.execute()


#Use: This is supposed to be alternative to graph.push(entities)
#Relationships done till now, nodes left
def push_with_cp(graph,*entities):
    cp=getNextCheckPoint(graph)
    stmt = push_with_cp_helper(graph,cp,entities)
    incrementCheckPoint(graph)
    return stmt


##TODO: test it completely and reduce database hits when possible.
##push only when actually pushing some changes to the nodes and relationships
##or else it will push exact same thing to the graph replicated with checkpointing
def push_with_cp_helper(graph,cp,*entities):
    for entity in entities[0]: #tuple
        if(isinstance(entity,Relationship)):
            #print 'here:' + str(entity.start_node)
            #print 'here2:' + str(entity.end_node)
            st=entity.start_node
            en=entity.end_node
            props=entity.properties
            typed=entity.type
            #print props["relid"]
            entity.unbind()
            old_rel = getLatestRelById(graph, props["relid"])
            old_rel["cp_end"]=str(int(cp)-1)
            #print old_rel.properties
            old_rel.push()
            new_rel=copyRelationship(props,st,en,typed)
            stmt = create_with_cp_helper(graph,cp,new_rel)
            #print new_rel.uri
            #print 'now: '+str(new_rel.bound)
            entity.bind(new_rel.uri)
            #print entity.uri
            return stmt
    

#Use : copyRelationship(properties_of_relation,start_node,end_node,type_of_relation), 
#returns a Relation copy exactly of the Relation in argument
#the returned relation is a copy of the props, dir, of the relation within same nodes needs to be pushed after this
def copyRelationship(props,st,en,typed):
    start = getLatestNodeById(graph,st["nodeid"])
    end=getLatestNodeById(graph,en["nodeid"])
    kind=typed
    r2=Relationship(start,kind,end)
    for x in props:
        r2[x]=props[x]
    return r2

##TESTS
def create_with_cpTest(graph):
    ##use case when multiple related nodes, to create a sub graph created
    a=Node("Person","Student",name="1")
    b=Node("Person","Student",name="2")
    c=Node("Person",name="3")
    c.labels.add("Student")
    r1=Relationship(a,"KNOWS",b)
    r2=Relationship(b,"KNOWS",c)
    r3=Relationship(c,"KNOWS",a)
    return create_with_cp(graph,a,b,c,r1,r2,r3) #push wont work here!!
#create_with_cpTest(graph) #TODO: save the descrption to the metadata


def push_with_cpTest(graph):
    ##use case when multiple related nodes, to create a sub graph created
    rel = getLatestRelById(graph,'1') #change accordingly
    print rel.uri
    rel["since"]=1999
    stmt  = push_with_cp(graph,rel)
    print rel.uri
    rel.pull() ##will have to do this for sure
    print rel["relid"]
    return stmt
#push_with_cpTest(graph) #TODO: save the descrption to the metadata
