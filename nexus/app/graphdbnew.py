from py2neo import Graph, Node, Relationship
import diff_match_patch
import pandas as pd


class GraphDB:

    def __init__(self,username, password, server, port):
        '''
            username = 'neo4j'
            password = '*'
            server = 'localhost'
            port = '7474'
        '''
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.con_url = 'http://'+username+':'+password+'@'+server+':'+port+'/db/data/' 
        self.graph = Graph(self.con_url)

    #Done: Multiple each time want to ask something
    #Else: works on old data only
    ##Wont use this
    def getGraph(self):
        return self.graph

    ##NOT TO BE USED
    #this is how we use the intenal ids of the graph
    ##should we use it?? most people say no
    ## anyways, made the method for future use
    ## Use : getNodeByInternalId(graph, 152)
    def getNodeByInternalId(self,id):
        a = self.graph.node(id) #getting by id given internally by neo4j
        a.pull()
        return a


    ##NOT TO BE USED
    ## similar to above
    ## Use : getRelByInternalId(graph, 4)
    def getRelByInternalId(self,id):
        a = self.graph.relationship(id)
        a.pull()
        return a
    
    
    def getNodeByUniqueID(self, idName, idVal, isIDString=False):
        ##TODO: move uuid to props
        query = "match (n {"
        if isIDString:
            query = query+ idName+":'"+str(idVal)+"'}) return n"
        else:
            query = query+ idName+":"+str(idVal)+"}) return n"
        rc = self.graph.cypher.execute(query)
        return rc[0][0]
    
    def getRelationByUniqueID(self, idName, idVal, isIDString=False):
        ##TODO: move uuid to props
        query = "match ()-[r {"
        if isIDString:
            query = query+ idName+":'"+str(idVal)+"'}]->() return r"
        else:
            query = query+ idName+":"+str(idVal)+"}]->() return r"
        rc = self.graph.cypher.execute(query)
        return rc[0][0]


    def isPropList(self, node, prop):
        return type(node[prop]) is list
    
    ##has a counter brother in nexusapis flask app    
    def isValidNonMetaProp(self, propname):
        if propname[0]=='_' or propname[-1]=='_':
            return False
        return True
    
    ##copy meta = True
    def copyNode(self, node, copymeta = True, exceptions = []):
        #exceptions are the props that should be included no matter what, if they have underscore or not!
        naya = Node()
        for label in node.labels:
            naya.labels.add(label)
        for prop in exceptions:
            if prop in node.properties:
                naya[prop] = node[prop]
        for prop in node.properties:
            if not copymeta:
                if self.isValidNonMetaProp(prop):
                    naya[prop] = node[prop]
            else:
                naya[prop] = node[prop]
        return naya
                
    def copyNodeAsItIs(self, node):
        return self.copyNode(node)
        #         naya = Node()
        #         for label in node.labels:
        #             naya.labels.add(label)
        #         for prop in node.properties:
        #             naya[prop] = node[prop]
        #         return naya
    
    def copyNodeWithoutMeta(self, node, exceptions=[]):
        return self.copyNode(node, copymeta = False, exceptions = exceptions)
    
    def copyRelation(self, rel, copymeta = True, rel_exceptions = [], node_exceptions = []):
        start_node  = ''
        end_node = ''
        
        if not copymeta:
            start_node = g.copyNodeWithoutMeta(rel.start_node, exceptions = node_exceptions)
            end_node = g.copyNodeWithoutMeta(rel.end_node, exceptions = node_exceptions)
        else:
            start_node = g.copyNodeAsItIs(rel.start_node)
            end_node = g.copyNodeAsItIs(rel.end_node)
            
        reltype = rel.type
        nayarel = Relationship(start_node, reltype, end_node)
        
        for prop in rel_exceptions:
            if prop in rel.properties:
                nayarel[prop] = rel[prop]
        for prop in rel.properties:
            if not copymeta:
                if self.isValidNonMetaProp(prop):
                    nayarel[prop] = rel[prop]
            else:
                nayarel[prop] = rel[prop]
        return nayarel
    
    def copyRelationAsItIs(self, rel):
        return self.copyRelation(rel)
        #         start_node = g.copyNodeAsItIs(rel.start_node)
        #         end_node = g.copyNodeAsItIs(rel.end_node)
        #         reltype = rel.type
        #         naya = Relationship(start_node, reltype, end_node)
        #         for prop in rel.properties:
        #             naya[prop] = rel[prop]
        #         return naya
    
    def copyRelationWithoutMeta(self, rel, rel_exceptions = [], node_exceptions = []):
        return self.copyRelation(rel, copymeta = False, rel_exceptions = rel_exceptions, node_exceptions = node_exceptions)

    ##example of some text input: (n154346:businessperson:person:politician {name:"Anita",uuid:1234})
    ##Usage: deserializeNode('''(n154346:businessperson:person:politician {name:"Anita",uuid:1234})''')
    def deserializeNode(self, nodeText):
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
        ##MAJOR TODO:
        ##work to do add a form where they can create a node
        #get a node's page by uuid
        #also get node's relations in form of graph, embed that graph
        #edit a node
        #edit a relation
        #dlete a node
        #delete a relation
        #moderate any change --> how to do that --> where will this lie!
        #Note the diff between now and then
        
    



class CoreGraphDB(GraphDB):
    
    def entity(self, uuid):
        return self.getNodeByUniqueID('uuid',uuid) ##isIDString by default false

    def relation(self, relid):
        return self.getRelationByUniqueID('relid', relid)
    
    def getNodeListCore(self, uuid_list):
        ans = []
        for c in uuid_list:
            ans.append(self.entity(c))
        return ans


    def labelsToBeAdded(self, orig, naya):
        new_labels = []
        for x in naya.labels:
            if x not in orig.labels:
                new_labels.append(x)
        return new_labels

    def propsDiff(self, orig, naya):
        conf_props = []
        new_props = []
        for x in naya.properties:
            if x not in orig.properties:
                new_props.append(x)
            else:
                conf_props.append(x)
        return conf_props, new_props


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
    def updatePrev(self, prev_uuid,latest):
        prev = entity(prev_uuid)
        prev_uuid = prev['uuid']
        prev.labels.clear()
        prev.properties.clear()
        for x in latest.labels:
            prev.labels.add(x)
        for x in latest.properties: #dont uupdate the uuid
            ##TODO move uuid to props
            if x!= 'uuid':
                prev[x]=latest[x]
        prev['uuid'] = prev_uuid
        prev.push() #also pushed
        #updated by now
        print 'The node with uuid '+str(prev_uuid)+' should be updated by now'

    def insertCoreNodeWrap(self, node):
        nodeText = node.__str__()
        node = self.deserializeNode(nodeText)
        ## use this table
        ## this table inside flasktemp for now
        ## create table uuidtable(uuid bigint(20) not null auto_increment primary key, name varchar(255));
        from dbwork import createUuid
        uuid = createUuid(node['name'])
        ##TODO: move uuid to props!
        print 'uuid generated ' +str(uuid)
        node['uuid'] = uuid
        print node
        self.graph.create(node)
        node.pull()
        return node



class SelectionAlgoGraphDB(GraphDB):
    
    def __init__(self,username, password, server, port):
        GraphDB.__init__(self,username, password, server, port)
        ##TODO: move these to constants.py when ipython not required
        self.metaprops = {'RESOLVEDUUID':'_resolvedWithUUID_','RESOLVEDRELID':'_resolvedWithRELID_'}
        
    def getFirstUnresolvedNode(self):
        results = []
        query = 'MATCH (n) where not exists(n.'+self.metaprops['RESOLVEDUUID'] +') ' +' return n limit 1'
        results = self.graph.cypher.execute(query)
        if len(results)==0:
            return None
        return results[0][0]
    
    def getRandomUnresolvedNode(self):
        results = []
        count = 0 ## 50  tries
        query = 'MATCH (n) WITH n WHERE rand() < 0.5 AND not exists(n.'+self.metaprops['RESOLVEDUUID'] +') ' 
        query = query +' return n limit 1'
        #print query
        while len(results) == 0 and count < 50:
            results = self.graph.cypher.execute(query)
            count = count + 1
        if len(results)==0: ##still!
            return None
        return results[0][0]
    
    def getHighestDegreeNode(self):
        ##TODO: get resolvedwithUUID out!
        query = 'start n = node(*) match (n)--(c) where not exists(n.'+self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'return n, count(*) as connections order by connections desc limit 1'
        #print query
        results = self.graph.cypher.execute(query)
        if len(results)==0: 
            return None, 0
        else:
            return results[0][0], results[0][1]
    
    def setResolvedWithUUID(self, node, uuid):
        node.properties[self.metaprops['RESOLVEDUUID']] = uuid
        node.push()
        
    def setResolvedWithRELID(self, rel, relid):
        rel.properties[self.metaprops['RESOLVEDRELID']] = relid
        rel.push()
        
    def getNearestBestNode(self):
        query = 'match (n)--(c) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(c.' + self.metaprops['RESOLVEDUUID'] +') ' 
        query = query + 'return c'
        maxdegree = 0
        maxnode = None
        for node in self.graph.cypher.execute(query):
            node = node[0]
            if maxdegree < node.degree:
                maxdegree = node.degree
                maxnode = node
        if maxdegree == 0:
            print '[SelectionAlgoGraphDB : nearest didnt work, working on highest]'
            maxnode,maxdegree = self.getHighestDegreeNode()
        if maxdegree == 0:
            print '[SelectionAlgoGraphDB: highest didnt work, working on first]'
            maxnode, maxdegree = self.getFirstUnresolvedNode(), 0
        return maxnode, maxdegree
    
    def getNextRelationToResolve(self):
        query = 'match (n)-[r]->(p) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') ' ##direction included
        query = query + 'AND exists(p.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return r limit 1'
        #print query
        results = self.graph.cypher.execute(query)
        if len(results)==0:
            return None
        else:
            return results[0][0]
        
    def countUnresolvedNodes(self): ##what is the reslut does not have anything?
        query = 'match n where not exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'return count(n)'
        results = self.graph.cypher.execute(query)
        return results[0][0]
    
    def countNextNodesToResolve(self): ##considers only the nodes that are connected rather than disconncted ones
        query = 'match (n)--(c) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(c.' + self.metaprops['RESOLVEDUUID'] +') ' 
        query = query + 'return count(c)'
        results = self.graph.cypher.execute(query)
        return results[0][0]
    
    def countUnresolvedRelations(self):
        query = 'match ()-[r]->() where not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return count(r)'
        results = self.graph.cypher.execute(query)
        return results[0][0]
    
    def countNextRelationsToResolve(self):
        query = 'match (n)-[r]->(p) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND exists(p.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return count(r)'
        #print query
        results = self.graph.cypher.execute(query)
        return results[0][0]