
# coding: utf-8


from py2neo import Graph, Node, Relationship

INFINITY = 9223372036854775807

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
    query = "match ()-[r {relid:"+str(ids)+",cp_end:"+str(INFINITY)+"}]-() return r"
    #print query
    rc = graph.cypher.execute(query)
    #print len(rc)
    #print rc
    return rc[0][0]

##Use: id used is what we have given by ourselves
##n1 = getLatestNodeById(graph, '1') # ##IndexError if not latest!! TODO
#print isinstance(n1,Node)
#n1
def getLatestNodeById(graph,ids):
    query = "match (n {nodeid:"+str(ids)+",cp_end:"+str(INFINITY)+"}) return n"
    rc = graph.cypher.execute(query)
    return rc[0][0]

##Use: getLastCheckPoint(graph)
## returns a string telling which was the last checkpoint in the graph
def getLastCheckPoint(graph): #returns a string
    a=graph.find_one('version_cp')
    return a.properties['next']-1

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
    a.properties['next'] = a.properties['next']+1
    a.push()
    return a

#Use: incrementNodeId(graph)
#to be used when a node with previous id has been created just now
def incrementNodeId(graph):
    a=graph.find_one('node_id')
    a.properties['next'] = a.properties['next']+1
    a.push()
    return a

#Use: incrementRelId(graph)
#to be used when a node with previous id has been created just now
def incrementRelId(graph):
    a=graph.find_one('rel_id')
    a.properties['next'] = a.properties['next']+1
    a.push()
    return a

#Use: delete_with_cp(graph,node1,node2,rel2,rel2)
##alternative to graph.delete(entities)
#will push any chnages that you have done! so beware that object should not be out of sync with server
#TODO MAJOR: delete is not that easy! if a current node is deleted and not its rels!!! then?
#  Solution should be: first del all rels in *entities, 
#  and then delete nodes -- if no live rels for these nodes outgoing incoming, only then else error 
def delete_with_cp(graph,*entities):
    for entity in entities: #to handle the tuple problem
        #patch to handle the delete issue
        #if a node is deleted now, that means it existed till last checkpoint
        entity["cp_end"]=getLastCheckPoint(graph)
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
        entity["cp_end"]=INFINITY
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
            
            #Rels that are alive do normal push
            if(old_rel["cp_end"]==INFINITY): 
                old_rel["cp_end"]=cp-1
                old_rel.push()
            ##else dead rels become live if this if is missing when reverting
                
            st.bind(st_uri)
            en.bind(en_uri)
            new_rel=copyRelationship(graph,props,st,en,typed)
            
            ##adding patch for keeping the relid same 
            new_rel["cp_start"]=cp
            new_rel["cp_end"]=INFINITY
            new_rel["relid"]=props["relid"]
            stmt = graph.create(new_rel)
            ##patch finished
            
            entity.bind(new_rel.uri)
            s+=str(stmt)
        elif(isinstance(entity,Node)):
            #find if a prev relation esxisted with NEXT
           
                
            #first push the new node just behind our current node
            entity["cp_start"] = cp #not psuhed yet
            entity["cp_end"] = INFINITY
            prev_uri= entity.uri
            nodeid=entity["nodeid"]
            entity.unbind()
            
            
            latest = ''
            old_node = getNodeAtHead(graph, nodeid)
            for r in old_node.match_incoming(rel_type="NEXT"):
                latest = r
                break
            
            new_node = copyNode(old_node)
            if(new_node["cp_end"]==INFINITY): #else if dead node: just copy as it is
                new_node["cp_end"]=cp-1
            new_rel = Relationship(new_node,"NEXT",old_node)
            stmt  = graph.create(new_node,new_rel)
            entity.bind(prev_uri)
            entity.push()
            s+=str(stmt)
            #now chnage pointers to make the new node scond last
            if(latest!=''):
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
    rel = getLatestRelById(graph,1) #change accordingly
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
    node = getLatestNodeById(graph,1) #change accordingly
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
    rel = getLatestRelById(graph,1) #change accordingly
    print rel.uri
    rel["since"]=1999
    
    node = getLatestNodeById(graph,1) #change accordingly
    print node.uri
    node["bye"]="last"
    
    stmt  = push_with_cp(graph,rel,node)
    
    rel.pull()
    node.pull()
    
    
    node=getLatestNodeById(graph,1) #change accordingly
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
    
    employee.pull()
    delete_with_cp(graph,first,second,employee)
    
    third=Node("Person",name="Abhishek Agarwal")
    create_with_cp(graph,third)

def test_limitInt(graph):
    node=Node("Random",prop=9223372036854775000)
    create_with_cp(graph,node)



##returns Relation which has custom id in 'ids' as we have given it
##and at this cp
def getRelByIdAndCheckPoint(graph,ids,cp):
    #TODO:Add check for cp in both these methods
    query = "match ()-[r {relid:"+str(ids)+"}]->() where r.cp_start <="+str(cp)+" and r.cp_end >="+str(cp)+" return r"
    #print query
    rc = graph.cypher.execute(query)
    if(len(rc)==0): return None ##TODO: make same changes to other get methods, if necessary
    return rc[0][0]

##Use: id used is what we have given by ourselves
#and at this cp
def getNodeByIdAndCheckPoint(graph,ids,cp):
    query = "match (n {nodeid:"+str(ids)+"}) where n.cp_start <="+str(cp)+" and n.cp_end >="+str(cp)+" return n"
    #print query
    rc = graph.cypher.execute(query)
    if(len(rc)==0): return None
    return rc[0][0]

def getNodeAtHead(graph,ids):
    query = "match (n {nodeid:"+str(ids)+"}) return n order by n.cp_end desc limit 1"
    rc = graph.cypher.execute(query)
    return rc[0][0]

def getRelAtHead(graph,ids):
    query = "match ()-[r {relid:"+str(ids)+"}]-() return r order by r.cp_end desc limit 1"
    rc = graph.cypher.execute(query)
    return rc[0][0]
    
##revert the graph to the checkpoint 'cp'
##gives a new cp to all reverted nodes and rels
def revert(graph,cp):
    
    #nextcp will be used if old nodes and rels are created back, so new cp nextcp is given to them
    nextcp = getNextCheckPoint(graph)
    
    #handling nodes first
    
    #store in noderc all nodes that've changed or born since said cp, these are the nodes we will work at 
    #all changed nodes need to be reverted back
    #all born nodes will become dead
    #born nodes also include nodes which were dead and made alive by previous revert, so they will become dead too, but catch is? just dead?? yes just dead. 
    #since born and zombie nodes were dead technically at that point of time
    nodequery = "match (n) where n.cp_start>"+str(cp)+" or (n.cp_end <> "+str(INFINITY)+" and "+str(cp)+"<=n.cp_end) return distinct n.nodeid"
    noderc = graph.cypher.execute(nodequery)
    
    #variable to tell us if we have to increment the cp, that is if any nodes/rels have actually been reverted back
    increment = False
    
    for r in noderc:
        
        #this query's response will differentiate between born and changed nodes
        #if old is None, node dint exist at that cp, and is existing now, make it dead
        #else existed then so revert now at any cost regardless of now dead or live, revert back
        old = getNodeByIdAndCheckPoint(graph,r['n.nodeid'],cp)
        #get at the head of the node list
        #will update this one
        #can be a dead node or live node
        naya = getNodeAtHead(graph,str(r['n.nodeid'])) 
        if old==None: #dead node at that cp, but first check if live right now, then make it dead, else let it be
            #same logic as in deleting #TODO: make a delete helper?
            ##existed till the previous checkpoint, from nextcp it is dead
            if (naya['cp_end']==INFINITY):
                ##this will happen : if live now and was dead at that time, kill it, with current props!
                ##why with current props? because state matters in this context not the props! think!! so this is good!
                naya['cp_end']=nextcp-1
                graph.push(naya)
            else:
                pass ##added to remove confusion
        else: #node was alive at that cp
            #copy all the props and labels from the old to naya and push with nextcp(use push_helper)
            if(old['cp_start']==naya['cp_start'] and old['cp_end']==naya['cp_end']): #case when node existed within that cp and vanished then
                push_with_cp_helper(graph,nextcp,naya)#only node
            else:
                naya.properties.clear()
                naya.labels.clear()
                for x in old.properties:
                    naya[x]=old[x]
                for x in old.labels:
                    naya.labels.add(x)
                push_with_cp_helper(graph,nextcp,naya)
        #increment in both cases
        increment = True
        if(naya.bound):
            naya.unbind()
        
    #same logic goes for relations
    relquery = "match ()-[r]->() where r.cp_start>"+str(cp)+" or (r.cp_end <> "+str(INFINITY)+" and "+str(cp)+"<=r.cp_end) return distinct r.relid"
    relrc = graph.cypher.execute(relquery)
    for r in relrc:
        old = getRelByIdAndCheckPoint(graph,r['r.relid'],cp)
        naya = getRelAtHead(graph,str(r['r.relid'])) ##TODO: change to get headoflinkedlist for dead nodes
        if old==None:
            ##existed till the previous checkpoint, from nextcp it is dead
            if(naya['cp_end']==INFINITY):
                naya['cp_end']=nextcp-1
                graph.push(naya)
        else:
            if(old['cp_start']==naya['cp_start'] and old['cp_end']==naya['cp_end']):
                push_with_cp_helper(graph,nextcp,naya)
            else:
                naya.properties.clear()
                for x in old.properties:
                    naya[x]=old[x]
                push_with_cp_helper(graph,nextcp,naya)
        #increment in both cases
        if(naya.bound):
            naya.unbind()
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
    gt.cypher.execute("create (n:version_cp:system {next:1}),   (p:node_id:system {next:1}),  (q:rel_id:system {next:1})")
    test_TwoNodesOneRelation(gt)
    revert(gt,'4')
    revert(gt,'8')
    revert(gt,'7')
    #test_intLimit(gt)
    #print getNodeByIdAndCheckPoint(gt,'3','6')
##TODO: graph wrapper for new methods
##Check django-neo4j and django-reversion
##Check neo-kafka
##Check method for serailizing and de-serailizing

##Check max what number can go in neo4j - no need for now, as string is working just fine, 
##we can create indices on cp_start and cp_end
##For a particular cp run a match query !!?? TODO? Match on previous nodes shouldnt be there! 
##Match always on latest nodes and relation! Never on deleted nodes
##TODO: Also check if node deleted, some changes elsewhere, now revert back to state where node existed
##Should give new number on reverting??
main()

