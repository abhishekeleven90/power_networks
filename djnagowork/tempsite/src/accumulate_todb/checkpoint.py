from py2neo import Graph, Node, Relationship

def getGraph(server,port,username,password):
    con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/'
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
    query = "match (n {nodeid:'"+ids+"',cp_end:'Infinity'}) return n"
    print query
    rc = graph.cypher.execute(query)
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

#Use: delete_with_cp(graph,node1,node2,rel2,rel2)
##alternative to graph.delete(entities)
#will push any chnages that you have done! so beware that object should not be out of sync with server
def delete_with_cp(graph,*entities):
    cp=getNextCheckPoint(graph)
    for entity in entities: #to handle the tuple problem
        entity["cp_end"]=cp
    graph.push(*entities) #the star was the catch here
    incrementCheckPoint(graph)


#Use: create_with_cp(graph,node1,node2,rel2,rel2)
##alternative to graph.create(entities)
def create_with_cp(graph,*entities):
    cp=getNextCheckPoint(graph)
    stmt = create_with_cp_helper(graph,cp,*entities)
    incrementCheckPoint(graph)
    return stmt

#Use: This method creates the entities with the checkpoint given in cp variable
#TODO: copied from core.py, make it easy
def create_with_cp_helper(graph,cp,*entities):
    from py2neo.cypher.create import CreateStatement
    statement = CreateStatement(graph)
    #print entities
    for entity in entities: #removed handle the tuple problem
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


#Use: This is supposed (to be alternative to graph.push(entities)
#Relationships done till now, nodes left
def push_with_cp(graph,*entities):
    cp=getNextCheckPoint(graph)
    stmt = push_with_cp_helper(graph,cp,*entities) ##TODO: add a true/false variable here that will help in deciding whether a push/revert
    incrementCheckPoint(graph)
    return stmt


##TODO: test it completely and reduce database hits when possible.
##push only when actually pushing some changes to the nodes and relationships
##or else it will push exact same thing to the graph replicated with checkpointing
def push_with_cp_helper(graph,cp,*entities):
    s=''
    for entity in entities: #removed the tuple problem now
        if(isinstance(entity,Relationship)):
            ##WARNING: deleting these print statements is a prob with py2neo!!!
            #print 'st:' + str(entity.start_node)+' --  en:' + str(entity.end_node)
            st=entity.start_node
            en=entity.end_node
            st_uri=entity.start_node.uri
            en_uri=entity.end_node.uri
            props=entity.properties
            typed=entity.type
            entity.unbind()
            old_rel = getRelAtHead(graph, props["relid"]) ##TODO: Use the cp_check variable here!
            old_rel["cp_end"]=str(int(cp)-1)
            old_rel.push()
            st.bind(st_uri)
            en.bind(en_uri)
            new_rel=copyRelationship(graph,props,st,en,typed)
            
            ##adding patch for keeping the relid same 
            new_rel["cp_start"]=cp
            new_rel["cp_end"]="Infinity"
            new_rel["relid"]=props["relid"]
            stmt = graph.create(new_rel)
            ##patch finished
            
            entity.bind(new_rel.uri)
            s+=str(stmt)
        elif(isinstance(entity,Node)):
            print 'nodenodenode'
            #find if a prev relation esxisted with NEXT
           
                
            #first push the new node just behind our current node
            entity["cp_start"] = cp #not psuhed yet
            entity["cp_end"] = "Infinity"
            prev_uri= entity.uri
            nodeid=entity["nodeid"]
            entity.unbind()
            
            
            latest = ''
            old_node = getNodeAtHead(graph, entity["nodeid"])
            for r in old_node.match_incoming(rel_type="NEXT"):
                latest = r
                break
            
            new_node = copyNode(old_node)
            new_node["cp_end"]=str(int(cp)-1)
            new_rel = Relationship(new_node,"NEXT",old_node)
            stmt  = graph.create(new_node,new_rel)
            entity.bind(prev_uri)
            entity.push()
            s+=str(stmt)
            #now chnage pointers to make the new node scond last
            if(latest!=''):
                print 'here'
                prev=latest.start_node
                prev.pull()
                new_node.pull()
                rel=Relationship(prev,"NEXT",new_node)
                graph.create(rel)
                print rel.bound
                graph.delete(latest)
                
    return s
            
    

#Use : copyRelationship(properties_of_relation,start_node,end_node,type_of_relation), 
#returns a Relation copy exactly of the Relation in argument
#the returned relation is a copy of the props, dir, of the relation within same nodes needs to be pushed after this
def copyRelationship(graph,props,st,en,typed):
    #print 'insidecopy:'+str(st) 
    start = getNodeAtHead(graph,st["nodeid"]) ##TODO: check if latestone needed??
    end=getNodeAtHead(graph,en["nodeid"])
    kind=typed
    r2=Relationship(start,kind,end)
    for x in props:
        r2[x]=props[x]
    return r2

#Use : copyNode(instance of a node) 
#returns a Node copy exactly of the Node in argument
#the returned relation is a copy of the props,labels of the node,  
#node will needs to be pushed after this
def copyNode(node):
    labels = node.labels
    props = node.properties
    naya=Node()
    for x in props:
        naya[x]=props[x]
    for x in labels:
        naya.labels.add(x)
    return naya

##INITIAL TESTS
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


##rel only
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


##node only
def push_with_cpTest2(graph):
    node = getLatestNodeById(graph,'1') #change accordingly
    print node.uri
    node["bye"]="last"
    stmt  = push_with_cp(graph,node)
    print node["nodeid"]
    node.pull() ##will have to do this for sure
    print node["nodeid"]
    return stmt


##rel only
def push_with_cpTest3(graph):
    ##use case when multiple related nodes, to create a sub graph created
    rel = getLatestRelById(graph,'1') #change accordingly
    print rel.uri
    rel["since"]=1999
    
    node = getLatestNodeById(graph,'1') #change accordingly
    print node.uri
    node["bye"]="last"
    
    stmt  = push_with_cp(graph,rel,node)
    
    rel.pull()
    node.pull()
    
    
    node=getLatestNodeById(graph,'1') #change accordingly
    print node.uri
    node["hi"]="new"
    
    push_with_cp(graph,node)
    return stmt
#push_with_cpTest(graph) #TODO: save the descrption to the metadata


##Disclaimer: Dont ever forget to pull the relations!! We fear even to test!
##Very basic tests to do
def test_OneNode(graph):
    
    #create first node
    first = Node("Politician","Person",name="Narendra Modi",age="56")
    create_with_cp(graph,first)
    
    #add a prop to first node
    first.pull()
    print first['nodeid']
    first['important']='true'
    push_with_cp(graph,first)
    
    #add a label
    first.pull()
    first.labels.add('IndianPrimeMinister')
    first['address']='Gujarat'
    push_with_cp(graph,first)
    
    #add a label and remove a label
    first.pull()
    first.labels.add('ChiefMinister')
    first.labels.remove('IndianPrimeMinister')
    push_with_cp(graph,first)
    
    #change a prop
    first.pull()
    first['name']='Narendra Damodar Modi'
    push_with_cp(graph,first)
    
    #remove a property
    first.pull()
    first.properties['age']=None
    push_with_cp(graph,first)
    
    #delete this node
    ##TODO: remove comment
    delete_with_cp(graph,first)
    

def test_TwoNodes(graph):
    
    #create nodes
    first = Node("Politician","Person",name="Narendra Modi",age="56")
    second = Node("Party","Organization",name="BJP")
    create_with_cp(graph,first,second)
    
    #add props
    first.pull()
    second.pull()
    first['live']='true'
    second['live']='true'
    push_with_cp(graph,first,second)
    
    #add labels
    first.pull()
    second.pull()
    first.labels.add('IndianPrimeMinister')
    first['address']='Gujarat'
    second.labels.add('PoliticalParty')
    second['address']='Delhi'
    push_with_cp(graph,first,second)
    
    #add a label and remove a label in both nodes
    first.pull()
    first.labels.add('ChiefMinister')
    first.labels.remove('IndianPrimeMinister')
    second.pull()
    second.labels.add('NationalParty')
    second.labels.remove('PoliticalParty')
    push_with_cp(graph,first,second)
    
    #change a prop
    first.pull()
    first['name']='Narendra Damodar Modi'
    second.pull()
    second['name']='Bhartiya Janta Party'
    push_with_cp(graph,first,second)
    
    #remove a property
    first.pull()
    first.properties['live']=None
    second.properties['live']=None
    push_with_cp(graph,first,second)
    
    #delete both nodes
    delete_with_cp(graph,first,second)
    
def test_TwoNodesOneRelation(graph):
    #create nodes
    first = Node("Politician","Person",name="Narendra Modi",age="56")
    second = Node("Party","Organization",name="BJP")
    employee = Relationship(first,"EmployeeOf",second)
    create_with_cp(graph,first,second,employee)
    
    #add props
    first.pull()
    second.pull()
    employee.pull()
    first['live']='true'
    second['live']='true'
    employee['current']='true'
    push_with_cp(graph,first,second,employee)
    
    
    #add labels, you cannot add another type or delete the previous type of a relation in neo4j
    first.pull()
    second.pull()
    employee.pull()
    first.labels.add('IndianPrimeMinister')
    first['address']='Gujarat'
    second.labels.add('PoliticalParty')
    second['address']='Delhi'
    employee['workingaddress']='CP'
    push_with_cp(graph,first,second,employee)
    
    
    #add a label and remove a label in both nodes
    first.pull()
    first.labels.add('ChiefMinister')
    first.labels.remove('IndianPrimeMinister')
    second.pull()
    second.labels.add('NationalParty')
    second.labels.remove('PoliticalParty')
    #doing no chnage to the relationship to see if nodes are updated and the relation old
    push_with_cp(graph,first,second)
    

    #change a prop
    first.pull()
    first['name']='Narendra Damodar Modi'
    second.pull()
    second['name']='Bhartiya Janta Party'
    employee.pull()
    employee['workingaddress']='Connaught Palace'
    push_with_cp(graph,first,second,employee)
    
    
    #remove a property
    first.pull()
    first.properties['live']=None
    second.pull()
    second.properties['live']=None
    employee.pull()
    employee.properties['current']=None
    push_with_cp(graph,first,second,employee)
    
    
    #delete both nodes and rels
    ##EVEN BEFORE DELETING A RELATION, you will have to pull
    ##this we can fix : TODO in delete method
    
    #employee.pull()
    #delete_with_cp(graph,first,second,employee)


##returns Relation which has custom id in 'ids' as we have given it
##and at this cp
def getRelByIdAndCheckPoint(graph,ids,cp):
    #TODO:Add check for cp in both these methods
    query = "match ()-[r {relid:'"+ids+"'}]-() where r.cp_start <='"+cp+"' and r.cp_end >='"+cp+"' return r"
    #print query
    rc = graph.cypher.execute(query)
    return rc[0][0]

##Use: id used is what we have given by ourselves
#and at this cp
def getNodeByIdAndCheckPoint(graph,ids,cp):
    query = "match (n {nodeid:'"+ids+"'}) where n.cp_start <='"+cp+"' and n.cp_end >='"+cp+"' return n"
    #print query
    rc = graph.cypher.execute(query)
    return rc[0][0]

def getNodeAtHead(graph,ids):
    query = "match (n {nodeid:'"+ids+"'}) return n order by n.cp_end desc limit 1"
    rc = graph.cypher.execute(query)
    return rc[0][0]

def getRelAtHead(graph,ids):
    query = "match ()-[r {relid:'"+ids+"'}]-() return r order by r.cp_end desc limit 1"
    rc = graph.cypher.execute(query)
    return rc[0][0]
    
def revert(graph,cp):
    nextcp = getNextCheckPoint(graph)
    nodequery = "match (n) where n.cp_start>'"+cp+"'  return distinct n.nodeid"
    noderc = graph.cypher.execute(nodequery)
    increment = False
    for r in noderc:
        old = getNodeByIdAndCheckPoint(graph,r['n.nodeid'],cp)
        naya = getNodeAtHead(graph,str(r['n.nodeid'])) ##TODO: change to get headoflinkedlist for dead nodes
        print naya
        naya.properties.clear()
        naya.labels.clear()
        for x in old.properties:
            naya[x]=old[x]
        for x in old.labels:
            naya.labels.add(x)
        push_with_cp_helper(graph,nextcp,naya)
        increment = True
    relquery = "match ()-[r]->() where r.cp_start>'"+cp+"'  return distinct r.relid"
    relrc = graph.cypher.execute(relquery)
    for r in relrc:
        old = getRelByIdAndCheckPoint(graph,r['r.relid'],cp)
        naya = getRelAtHead(graph,str(r['r.relid'])) ##TODO: change to get headoflinkedlist for dead nodes
        naya.properties.clear()
        for x in old.properties:
            naya[x]=old[x]
        push_with_cp_helper(graph,nextcp,naya)
        increment = True
    if increment:
        incrementCheckPoint(graph)

def main():
    ###
    #   To setup the system:
    ## create (n:version_cp:system {next:'1'}),   (p:node_id:system {next:'1'}),  (q:rel_id:system {next:'1'})
    ##

    ##first delete all the nodes and rels that are in the db
    ##or change the db for better
    gt=getGraph('localhost','7474','neo4j','yoyo')
    gt.delete_all()
    gt.cypher.execute("create (n:version_cp:system {next:'1'}),   (p:node_id:system {next:'1'}),  (q:rel_id:system {next:'1'})")
    test_TwoNodesOneRelation(gt)
    revert(gt,'3')
##TODO: graph wrapper for new methods
##Check django-neo4j and django-reversion
##Check neo-kafka
##Check method for serailizing and de-serailizing

##Check max what number can go in neo4j
##For a particular cp run a match query !!?? TODO? Match on previous nodes shouldnt be there! 
##Match always on latest nodes and relation! Never on deleted nodes
##TODO: Also check if node deleted, some changes elsewhere, now revert back to state where node existed
##Should give new number on reverting??
main()
