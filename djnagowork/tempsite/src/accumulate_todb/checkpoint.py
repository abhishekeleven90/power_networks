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
    #create_with_cpTest(gt)
    #push_with_cpTest3(gt)
    test_TwoNodesOneRelation(gt)

##TODO: relids are being generated again and again, should we do this? nodeids are being kepth the same
##TODO: graph wrapper for new methods
##Test various scenarios
##Make api for node,rel at a particular checkpoint
##Make api for reverting graph to a particular state, can be done
##Check django-neo4j and django-reversion
##Check neo-kafka
##Check method for serailizing and de-serailizing
#
#gt=getGraph('localhost','7474','neo4j','yoyo')aaa=Node()
#main()
