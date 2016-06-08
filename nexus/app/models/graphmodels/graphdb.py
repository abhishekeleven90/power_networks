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

         ##TODO: move these to constants.py when IPYTHON not required
        self.metaprops = {
        'RESOLVEDUUID':'_resolvedWithUUID_',
        'RESOLVEDRELID':'_resolvedWithRELID_',
        'RESOLVEDHENID':'_resolvedWithHENID_', ##for hyper edge node
        'RESOLVEDHERID':'_resolvedWithHERID_', ##for hyper edge relation
        }

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
    
    
    def getNodeByUniqueID(self, uniquelabel, idName, idVal, isIDString=False):
        ##TODO: move uuid to props
        query = "match (n:"+uniquelabel+" {"
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
            start_node = self.copyNodeWithoutMeta(rel.start_node, exceptions = node_exceptions)
            end_node = self.copyNodeWithoutMeta(rel.end_node, exceptions = node_exceptions)
        else:
            start_node = self.copyNodeAsItIs(rel.start_node)
            end_node = self.copyNodeAsItIs(rel.end_node)
            
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

    def getDirectlyConnectedEntities(self, idname, idval, uniquelabel='', isIDString = True):
        '''
            given idname like uuid, henid and uniquelabel like entity or hyperedgenode
            gives us the connected nodes of this node
            returns nodes which have uuids only
            note: works for hyperedgenodes only for now
            #TODO: extend so that this info can be shown on view page
        '''
        from app.constants import LABEL_ENTITY
        invertedComma = ''
        if isIDString:
            invertedComma = "'"
        query = "match (n:%s {%s:%s%s%s})-[]-(p:%s) return distinct(p)"
        query = query %(uniquelabel, idname, invertedComma, idval, invertedComma, LABEL_ENTITY)
        results = self.graph.cypher.execute(query)
        enlist = []
        for res in results:
            enlist.append(res[0])
        return enlist


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

    def generateSearchData(self, idname, idval, isIDString, getList=False):

        from app.utils.commonutils import Utils
        utils  = Utils()

        comp = self.getNodeByUniqueID('entity', idname, idval, isIDString)
        ##comp is the node in question
        
        keywords = ''
        labels = ''
        aliases_to_return = ''

        if getList:
            keywords = []
            labels = []
            aliases_to_return = []

        quotes = "" ##the ' wre  reudundant from beginning

        for prop in comp.properties:
            ##begins with underscore ignore
            if prop!='uuid' and prop!='aliases' and prop[0]!='_':
                currvalue = str(comp.properties[prop])
                currvalue = utils.processString(currvalue)
                if prop!='uuid' and len(currvalue)>3:
                    if not getList:
                        keywords = keywords + quotes +currvalue + quotes+","
                    else:
                        keywords.append(currvalue)

        neighbours  = self.getDirectlyConnectedEntities(idname, idval, 
            'entity', isIDString)

        for rel in neighbours:
            currvalue = str(rel.properties['name'])
            currvalue = utils.processString(currvalue)
            if not getList:
                keywords = keywords + quotes +rel.properties['name'] + quotes+","
            else:
                keywords.append(rel.properties['name'])
        # keywords = keywords + '"'

        # labels = ''
        for label in list(comp.labels):
            if not getList:
                labels = labels + quotes + label + quotes+","
            else:
                labels.append(label)
        # labels=labels + '"'
        
        aliases = comp['aliases']
        
        if aliases is None or aliases == []:
            aliases = [comp['name']]

        # aliases_to_return = '"'
        # aliases_to_return = ''

        for alias in aliases:
            if not getList:
                aliases_to_return = aliases_to_return + quotes +alias + quotes+","
            else:
                aliases_to_return.append(alias)
        # aliases =aliases_to_return + '"'
        
        # name = '"'+comp.properties['name']+'"'
        name = comp.properties['name']
        
        return name, labels, aliases_to_return, keywords


class CoreGraphDB(GraphDB):

    def __init__(self):
        
        from app.constants import CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD, CORE_GRAPH_PORT, CORE_GRAPH_USER

        GraphDB.__init__(self, username = CORE_GRAPH_USER, password = CORE_GRAPH_PASSWORD, server = CORE_GRAPH_HOST, port = CORE_GRAPH_PORT)
    
    def entity(self, uuid):
        return self.getNodeByUniqueID('entity','uuid',uuid) ##isIDString by default false

    def relation(self, relid):
        return self.getRelationByUniqueID('relid', relid)

    def hyperedgenode(self, henid):
        return self.getNodeByUniqueID('hyperedgenode','henid',henid) ##isIDString by default false    
    
    def getNodeListCore(self, uuid_list):
        ans = []
        for c in uuid_list:
            ans.append(self.entity(c))
        return ans

    ##TODO: merge getNodeListCore and getRelListCore seem similar!
    def getRelListCore(self, relid_list):
        ans = []
        for c in relid_list:
            ans.append(self.relation(c))
        return ans

    def labelsToBeAdded(self, orig, naya):
        new_labels = []
        for x in naya.labels:
            if x not in orig.labels:
                new_labels.append(x)
        return new_labels

    def propsDiff(self, orig, naya):
        from app.constants import MVPLIST
        conf_props = []
        new_props = []
        #mvp_props = []
        for x in naya.properties:

            # if x in MVPLIST: 
            #     if type(naya[x]) is list:
            #     mvp_props.append(x)


            if x not in orig.properties:
                new_props.append(x)
            else:
                # if orig[x] != naya[x]: 
                ##exactly equal prop! TODO: if all props equal -> empty,

                #TODO:
                ## then submit doesnt allow to go any further
                ##will have to check no new labels, no new props, no new conf props, 
                ##go to next method, that is show-->home page of verifier
                ##no point in any clicks

                ##TODO: disallow some props to come?
                #conf_props.append(x)
                conf_props.append(x)
        return conf_props, new_props #mvp_props


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

    def insertCoreNodeWrapGeneric(self, node, idprop, idval):
        node = self.copyNodeAsItIs(node)
        node[idprop] = idval
        print node
        self.graph.create(node)
        node.pull()
        return node

    def insertCoreNodeWrap(self, node, uuid):
        from app.constants import CORE_GRAPH_UUID
        return self.insertCoreNodeWrapGeneric(node, CORE_GRAPH_UUID, uuid)

    def insertCoreHyperEdgeNodeWrap(self, hyperedgenode, henid):
        from app.constants import CORE_GRAPH_HENID
        return self.insertCoreNodeWrapGeneric(hyperedgenode, CORE_GRAPH_HENID, henid)

    def insertCoreRelWrap(self, rel, start_node_uuid, end_node_uuid, relid):

        print 'inside graph db work - relid ' +str(relid)

        start_node = self.entity(start_node_uuid)
        end_node = self.entity(end_node_uuid)

        #construct the relation object
        newrel = Relationship(start_node,rel.type,end_node)

        #copy the props
        for prop in rel.properties:
            newrel[prop] = rel[prop]
        newrel['relid'] = relid ##TODO: db work here!
        #in the end just copy the new relation id
    
        self.graph.create(newrel) ##create the actual graph object!
        newrel.pull()
        return newrel

    def searchRelations(self, start_node_uuid, reltype, end_node_uuid,):
        ##note that the direction has been kept intact
        ##note that this is very basic search but 
        ##we wont have much relations between two nodes
        query = "match (n {uuid:%s})-[r:%s]->(p {uuid:%s}) return r"
        query = query %(start_node_uuid, reltype, end_node_uuid)
        results = self.graph.cypher.execute(query)
        rellist = []
        for res in results:
            rellist.append(res[0])
        return rellist

    def searchHyperEdgeNodes(self, labels, enuuids):
        ##note that direction does not matter our relation matters here
        #one to one relation exists between all and hyperedgenode
        query = ''
        print enuuids
        for uuid in enuuids:
            q = "match (n:%s:%s)-[]-(:entity {uuid:%s}) "
            q = q %(labels[0], labels[1], uuid)
            query = query + q
        query = query + ' return n'
        print query
        results = self.graph.cypher.execute(query)
        henlist = []
        for res in results:
            henlist.append(res[0])
        return henlist

    def generateNewUUID(self):
        results = self.graph.cypher.execute('match (n:_meta_ {metaid:1}) with n,n.nextuuid as nextuuid set n.nextuuid=n.nextuuid+1 return nextuuid')
        return results[0][0]
    
    def generateNewRELID(self):
        results = self.graph.cypher.execute('match (n:_meta_ {metaid:1}) with n,n.nextrelid as nextrelid set n.nextrelid=n.nextrelid+1 return nextrelid')
        return results[0][0]

    def generateIndexData(self, uuid):

        '''
            As soon as you update en entity or insert an entity, call this to get the change on props
            As soon as you create a rel and you know the startuuid and newuuid, call this on both
            Use this to update the concerned entities in indexdb for solr
        '''

        ##MAJOR TODO: change to use seatchdata
        return self.generateSearchData('uuid', uuid, False)
        
        # q = "MATCH (p:entity {uuid:"+str(uuid)+"}) RETURN p"
        # keywords = '"'
        # comp = graph.cypher.execute(q)
        # comp = comp[0][0]
        # for prop in comp.properties:
        #     if prop!='uuid' and prop!='aliases':
        #         currvalue = str(comp.properties[prop])
        #         currvalue = processString(currvalue)
        #         if prop!='uuid' and len(currvalue)>3:
        #             keywords = keywords + "'" +currvalue + "',"
            
        
        # q = "match (n:entity {uuid:"+str(uuid)+"})-[r]-(p) return distinct(p)"
        # rels = graph.cypher.execute(q)
        # for rel in rels:
        #     rel =  rel[0]
        #     currvalue = str(rel.properties['name'])
        #     currvalue = processString(currvalue)
        #     keywords = keywords + "'" +rel.properties['name'] + "',"
        # keywords = keywords + '"'
        
        # labels = '"'
        # for label in list(comp.labels):
        #     labels = labels +"'"+label + "',"
        # labels=labels + '"'
        
        # aliases = comp['aliases']
        # aliases_to_return = '"'
        # for alias in aliases:
        #     aliases_to_return = aliases_to_return + "'" +alias + "',"
        # aliases =aliases_to_return + '"'
        
        # name = '"'+comp.properties['name']+'"'
        
        # return name, labels, aliases, keywords
    

class SelectionAlgoGraphDB(GraphDB):
    
    def __init__(self):

        from app.constants import CRAWL_GRAPH_HOST, CRAWL_GRAPH_PASSWORD, CRAWL_GRAPH_PORT, CRAWL_GRAPH_USER

        GraphDB.__init__(self, username = CRAWL_GRAPH_USER, password = CRAWL_GRAPH_PASSWORD, server = CRAWL_GRAPH_HOST, port = CRAWL_GRAPH_PORT)

       
        
    def getFirstUnresolvedNode(self):
        from app.constants import LABEL_ENTITY
        results = []
        query = 'MATCH (n:'+LABEL_ENTITY+') where not exists(n.'+self.metaprops['RESOLVEDUUID'] +') ' +' return n limit 1'
        results = self.graph.cypher.execute(query)
        if len(results)==0:
            return None
        return results[0][0]
    
    def getRandomUnresolvedNode(self):
        from app.constants import LABEL_ENTITY
        results = []
        count = 0 ## 50  tries
        query = 'MATCH (n:'+LABEL_ENTITY+') WITH n WHERE rand() < 0.5 AND not exists(n.'+self.metaprops['RESOLVEDUUID'] +') ' 
        query = query +' return n limit 1'
        #print query
        while len(results) == 0 and count < 50:
            results = self.graph.cypher.execute(query)
            count = count + 1
        if len(results)==0: ##still!
            return None
        return results[0][0]
    
    def getHighestDegreeNode(self):
        from app.constants import LABEL_ENTITY
        ##TODO: get resolvedwithUUID out!
        query = 'start n = node(*) match (n:'+LABEL_ENTITY+')--(c) where not exists(n.'+self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'return n, count(*) as connections order by connections desc limit 1'
        ##note that according to this query, c can be a hyperedge node too.
        #print query
        results = self.graph.cypher.execute(query)
        if len(results)==0: 
            return None, 0
        else:
            return results[0][0], results[0][1]
    
    def setResolvedWithUUID(self, node, uuid):
        node.properties[self.metaprops['RESOLVEDUUID']] = uuid
        node.push()

    def setResolvedWithHENID(self, hyperedgenode, henid):
        hyperedgenode.properties[self.metaprops['RESOLVEDHENID']] = henid
        hyperedgenode.push()
        
    def setResolvedWithRELID(self, rel, relid):
        rel.properties[self.metaprops['RESOLVEDRELID']] = relid
        rel.push()
        
    def getNearestBestNode(self):
        from app.constants import LABEL_ENTITY
        query = 'match (n:'+LABEL_ENTITY+')--(c:'+LABEL_ENTITY+') where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(c.' + self.metaprops['RESOLVEDUUID'] +') ' 
        #query = query + "AND not '"+HYPEREDGE_NODE_LABEL+"'' in labels(c) " 
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
        ##TODO: use constant here for entity
        query = 'match (n:entity)-[r]->(p:entity) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') ' ##direction included
        query = query + 'AND exists(p.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return r limit 1'
        #print query
        results = self.graph.cypher.execute(query)
        if len(results)==0:
            return None
        else:
            return results[0][0]

    def getNearestBestHyperEdgeNode(self):
        from app.constants import LABEL_HYPEREDGE_NODE, LABEL_ENTITY
        query = 'match (n:'+LABEL_ENTITY+')--(c:'+LABEL_HYPEREDGE_NODE+') where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(c.' + self.metaprops['RESOLVEDHENID'] +') ' 
        query = query + 'return c limit 1' ##distinct c or unique c?
        results = self.graph.cypher.execute(query)
        if len(results)==0:
            return None
        else:
            return results[0][0]
        
        
    def countUnresolvedNodes(self): ##what is the reslut does not have anything?
        from app.constants import LABEL_ENTITY
        query = 'match (n:'+LABEL_ENTITY+') where not exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'return count(n)'
        results = self.graph.cypher.execute(query)
        return results[0][0]
    
    def countNextNodesToResolve(self): ##considers only the nodes that are connected rather than disconncted ones
        from app.constants import LABEL_ENTITY
        query = 'match (n:'+LABEL_ENTITY+')--(c:'+LABEL_ENTITY+') where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(c.' + self.metaprops['RESOLVEDUUID'] +') ' 
        query = query + 'return count(c)'
        results = self.graph.cypher.execute(query)
        return results[0][0]

    def countUnresolvedHyperEdgeNodes(self):
        '''counts the number of hyperedgenodes in current crawled graph that have to be resolved'''
        from app.constants import LABEL_HYPEREDGE_NODE
        query = 'match (n:'+LABEL_HYPEREDGE_NODE+') where not exists(n.' + self.metaprops['RESOLVEDHENID'] +') '
        query = query + 'return count(n)'
        results = self.graph.cypher.execute(query)
        return results[0][0]

    def countNextHyperEdgeNodesToResolve(self): ##considers only the nodes that are connected rather than disconncted ones
        '''
            first counts the nodes that cannot be resolved immediately
            then using unresolvedhens - this count, gives the result.
            was a major bug, took a lot of time, to correctly do this using cypher  
        '''
        from app.constants import LABEL_HYPEREDGE_NODE, LABEL_ENTITY
        RESOLVEDHENID = self.metaprops['RESOLVEDHENID']
        RESOLVEDUUID = self.metaprops['RESOLVEDUUID']
        query = 'match (c:%s) where not exists(c.%s) with c' 
        query = query + ' match (n:%s)--(c) where not exists(n.%s) with c, count(n) as countn'
        query = query + ' where countn <> 0 return count(distinct c) '
        query = query %(LABEL_HYPEREDGE_NODE, RESOLVEDHENID, LABEL_ENTITY, RESOLVEDUUID)
        print 'hhhhhhhhhhhh'
        print query
        results = self.graph.cypher.execute(query)
        count =  results[0][0]
        return self.countUnresolvedHyperEdgeNodes() - count

    
    def countUnresolvedRelations(self):
        ##TODO: use constant here for entity
        ##only this one would have been affacted since hyperedgelink has been introduced
        from app.constants import LABEL_ENTITY
        query = 'match (:entity)-[r]->(:entity) where not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return count(r)'
        results = self.graph.cypher.execute(query)
        return results[0][0]
    
    def countNextRelationsToResolve(self):
        ##TODO: use constant here for entity
        query = 'match (n:entity)-[r]->(p:entity) where exists(n.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND exists(p.' + self.metaprops['RESOLVEDUUID'] +') '
        query = query + 'AND not exists(r.' + self.metaprops['RESOLVEDRELID'] +') '
        query = query + 'return count(r)'
        #print query
        results = self.graph.cypher.execute(query)
        return results[0][0]

    def copyRelationWithEssentialNodeMeta(self, rel):
        return self.copyRelationWithoutMeta(rel, node_exceptions=[self.metaprops['RESOLVEDUUID']]) 



class GraphObject():

    def __init__(self, coredb):
        self.coredb = coredb
        self.crawldb = crawldb
        ##so can handle graphdb throough that

    def getCoreIDName(self): ##could have been class method as such but still ok
        pass

    def getCrawlIDName(self):
        pass

    def getDirectlyConnectedEntities(self):
        pass

    def setResolvedWithID(self, curr_id):
        ##only on crawldb
        pass

    def insertCoreGraphObjectHelper(self):
        pass

