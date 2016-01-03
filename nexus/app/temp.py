from py2neo import Graph, Node, Relationship
import diff_match_patch

username = 'neo4j'
password = 'yoyo'
server = 'localhost'
port = '7474'
con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/'


def getGraph():
#return a graph by con_url
    graph = Graph(con_url)
    return graph

#this is how we use the intenal ids of the graph
##should we use it?? most people say no
## anyways, made the method for future use
## Use : getNodeByInternalId(graph, 152)
def getNodeByInternalId(graph,id):
	a = graph.node(id) #getting by id given internally by neo4j
	a.pull()
	return a


## similar to above
## Use : getRelByInternalId(graph, 4)
def getRelByInternalId(graph,id):
	a = graph.relationship(id)
	a.pull()
	return a

def createNodes(graph):
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


def createNodes2(graph):
	alice = Node("Party", name="Alice")
	alice2 = Node("Party", name="Alicehaha", age="34")
	bob = Node("Politician", name="Bob")
	alice_knows_bob = Relationship(alice, "related", bob)
	calice = str(alice)
	calice2 = str(alice2)

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


def getNodeByUuid(graph):
	pass

##work to do add a form where they can create a node
#get a node's page by uuid
#also get node's relations in form of graph, embed that graph
#edit a node
#edit a relation
#dlete a node
#delete a relation
#moderate any change --> how to do that --> where will this lie!
#Note the diff between now and then