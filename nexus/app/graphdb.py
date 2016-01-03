from py2neo import Graph, Node, Relationship
import diff_match_patch

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

##NOT TO BE USED
#this is how we use the intenal ids of the graph
##should we use it?? most people say no
## anyways, made the method for future use
## Use : getNodeByInternalId(graph, 152)
def getNodeByInternalId(graph,id):
	a = graph.node(id) #getting by id given internally by neo4j
	a.pull()
	return a


##NOT TO BE USED
## similar to above
## Use : getRelByInternalId(graph, 4)
def getRelByInternalId(graph,id):
	a = graph.relationship(id)
	a.pull()
	return a

def createNodes2(graph):
	alice = Node("Party", name="Alice")
	alice2 = Node("Party", name="Alicehaha", age="34")
	bob = Node("Politician", name="Bob")
	alice_knows_bob = Relationship(alice, "related", bob)
	calice = str(alice)
	calice2 = str(alice2)
	print calice
	print calice2

	print bob
	print alice_knows_bob
	graph.create(alice_knows_bob)


def createNodes(graph):
	from py2neo.cypher import CypherWriter
	import sys
	writer = CypherWriter(sys.stdout)
	alice = Node("Party","Politician","Director", name="Alice")
	alice2 = Node("Party", name="Alicehaha", age="34")
	bob = Node("Politician", name="Bob")
	alice_knows_bob = Relationship(alice, "related", bob)
	some = writer.write(alice)
	print 'printing Some\n'
	print some
	calice = str(alice)
	calice2 = str(alice2)
	
	print alice
	print 'herehfhgfhgfdgjdgfhgggggggggggggggggggggg'
	nodenaya = ''
	print nodenaya
	print 'theredkhfhgffgggggggggggggggg'

	#help from: http://agiliq.com/blog/2014/05/google-diff-match-patch-library/

	
	diff_obj = diff_match_patch.diff_match_patch()
	diffs = diff_obj.diff_main(calice, calice2)
	diff_obj.diff_cleanupSemantic(diffs)
	print 'now the diff here'
	print str(diffs)
	html = diff_obj.diff_prettyHtml(diffs)

	print 'some more expreiment'
	diff_obj = SideBySideDiff()
	result = diff_obj.diff_main(calice, calice2)
	diff_obj.diff_cleanupSemantic(result)

	old_record = diff_obj.old_content(result) 
	new_record = diff_obj.new_content(result)

	print bob
	print alice_knows_bob
	graph.create(alice_knows_bob)
	return old_record,new_record


class SideBySideDiff(diff_match_patch.diff_match_patch):

    def old_content(self, diffs):
        """
        Returns HTML representation of 'deletions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

            if flag == self.DIFF_DELETE:
                html.append("""<del style=\"background:#ffe6e6;
                    \">%s</del>""" % text)
            elif flag == self.DIFF_EQUAL:
                html.append("<span>%s</span>" % text)
        return "".join(html)

    def new_content(self, diffs):
        """
        Returns HTML representation of 'insertions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))
            if flag == self.DIFF_INSERT:
                html.append("""<ins style=\"background:#e6ffe6;
                    \">%s</ins>""" % text)
            elif flag == self.DIFF_EQUAL:
                html.append("<span>%s</span>" % text)
        return "".join(html)

def entity(uuid):
	query = "match (n {uuid:"+str(uuid)+"}) return n"
	rc = graph.cypher.execute(query)
	return rc[0][0]

def relation(relid):
	query = "match ()-[r {relid:"+str(relid)+"}]-() return r"
	#print query
	rc = graph.cypher.execute(query)
	#print len(rc)
	#print rc
	return rc[0][0]


#prev is a Node
#latest is a Node
#Usage:
'''
alice = Node("Ola","Olap","Olat", name="uinq",uuid=4)
print alice
bob = Node("Person","Politician", name="bob",uuid=4)
print bob
updatePrev(alice,bob)
print alice
'''
def updatePrev(prev_uuid,latest):
    prev = entity(prev_uuid)
    prev_uuid = prev['uuid']
    prev.labels.clear()
    prev.properties.clear()
    for x in latest.labels:
        prev.labels.add(x)
    for x in latest.properties: #dont uupdate the uuid
        if x!= 'uuid':
            prev[x]=latest[x]
    prev['uuid'] = prev_uuid
    prev.push() #also pushed
    #updated by now
    print 'The node with uuid '+str(prev_uuid)+' should be update by now'


##example of some text input: (n154346:businessperson:person:politician {name:"Anita",uuid:1234})
##Usage: deserializeNode('''(n154346:businessperson:person:politician {name:"Anita",uuid:1234})''')
def deserializeNode(nodeText):
    pos =  nodeText.find(' ')
    
    #get the labels in a set
    startText = nodeText[1:pos]
    allLabels = startText.split(':')[1:]
    allLabels =  set(allLabels) #set is imp
    
    #get the props in a dict
    endText = nodeText[pos+1:-1]
    endTextWB = endText[1:-1]
    #print endText
    #print endTextWB
    propList = endTextWB.split(",")
    propsDict = {}
    for x in propList:
        propval = x.split(":")
        #for handling the single inverted comma problem
        prop = propval[0]
        val = propval[1]
        if val[0]=="'" and val[-1]=="'":
            val=val[1:-1]
        #for handling the double inverted comma problem
        if val[0]=='"' and val[-1]=='"':
            val=val[1:-1]
        propsDict[prop]=val

    
    #print propsDict
    
    #creating the node from parsedText
    node = Node()
    for x in allLabels:
        node.labels.add(x)
    for x in propsDict:
        node[x] = propsDict[x]
    print node
    return node



##work to do add a form where they can create a node
#get a node's page by uuid
#also get node's relations in form of graph, embed that graph
#edit a node
#edit a relation
#dlete a node
#delete a relation
#moderate any change --> how to do that --> where will this lie!
#Note the diff between now and then