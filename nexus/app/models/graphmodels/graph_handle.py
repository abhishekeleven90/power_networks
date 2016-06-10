from app.models.graphmodels.graphdb import SelectionAlgoGraphDB, CoreGraphDB
from flask import current_app


class GraphHandle():
    
    """Business logic for dealing with graph and querying the right graph"""

    def __init__(self):
        
        self.crawldb = SelectionAlgoGraphDB()

        self.coredb = CoreGraphDB()

    def getCrawlNodeStats(self):
        return self.crawldb.countUnresolvedNodes(), self.crawldb.countNextNodesToResolve()

    def getCrawlRelationStats(self):
        return self.crawldb.countUnresolvedRelations(), self.crawldb.countNextRelationsToResolve()

    def getCrawlHyperEdgeNodeStats(self):
        return self.crawldb.countUnresolvedHyperEdgeNodes(), self.crawldb.countNextHyperEdgeNodesToResolve()

    def areCrawlNodesLeft(self):
        n1,n2 = self.getCrawlNodeStats()
        return n1 != 0 ##here the first count can work as we just need to select any node

    def areCrawlHyperEdgeNodesLeft(self):
        n1,n2 = self.getCrawlHyperEdgeNodeStats()
        return n1 != 0 ##here the first count can work as we just need to select any hyper edge node

    def areCrawlRelationsLeft(self):
        r1,r2 = self.getCrawlRelationStats()
        return r2 != 0  ##here the second count works as we just need to select any relation for which the nodes are resolved

    def updateCrawlNode(self, node, uuid):
        self.crawldb.setResolvedWithUUID(node, uuid)

    def updateCrawlRelation(self, rel, uuid):
        self.crawldb.setResolvedWithRELID(self, rel, relid)

    def nextNodeToResolve(self, userid):

        ##can put a check here to see if all nodes locked at moment
        ##dont proceed further

        # ##no longer would be required
        # count = self.crawldb.countNotLockedUnresolvedNodes() 
        # if count == 0:
        #     return None

        node, degree =  self.crawldb.getNearestBestNode()
        
        if node is None:
            ##all nodes resolved or locked -  by new changes
            ##no node to resolve
            return node ##returns a type py2neo.Node, can be None

        node = self.crawldb.lockObject(node, userid)

        if node is None:
            ##was already locked if goes in this condition
            node = self.nextNodeToResolve(userid)
            return node

        return node

    def nextHyperEdgeNodeToResolve(self, userid):
        #TODO: remove prints
        node =  self.crawldb.getNearestBestHyperEdgeNode()
        print 'hyperedgenode selected'
        print node
        return node ##returns a type py2neo.Node, can be None

    def nextRelationToResolve(self, userid):
        rel =  self.crawldb.getNextRelationToResolve()
        if rel is None:
            return rel
        
        rel = self.crawldb.lockObject(rel, userid)
        if rel is None:
            rel = self.nextRelationToResolve(userid)
            return rel
        
        return rel ##returns a type py2neo.relation, can be None

    def getNodeListCore(self, uuidList):
        return self.coredb.getListOfNodes(uuidList)


    def deltaIndexDBHelper(self):
        from app.solr.SolrIndex import delta_import
        delta_import()


    def insertToIndexDBHelper(self, uuid):
        name, labels, aliases, keywords = self.coredb.generateIndexData(uuid)
        from app.models.dbmodels.index_entities import Entity
        en = Entity(uuid=uuid, name=name, aliases=aliases, keywords =keywords, labels= labels)
        rows =  str(en.insertEntity())
        self.deltaIndexDBHelper()
        return rows

    def updateIndexDBHelper(self, uuid):
        name, labels, aliases, keywords = self.coredb.generateIndexData(uuid)
        from app.models.dbmodels.index_entities import Entity
        en= Entity()
        en.getEntity(uuid)
        en.name = name
        en.labels = labels
        en.aliases = aliases
        en.keywords = keywords
        rows = str(en.updateEntity())
        self.deltaIndexDBHelper()
        return rows

    def insertCoreNodeHelper(self, node):
        ##a very basic necessity of this! 
        ##as uuids and graphs are linked 

        uuid = self.coredb.generateNewUUID()
        #in case of any mishap: 
        #first check: match (n:_meta_ {metaid:1}) return n.nextuuid
        #match (n:_meta_ {metaid:1}) set n.nextuuid = n.nextuuid -1 return n.nextuuid

        from app.models.dbmodels.uuidtable import UUIDTable
        en = UUIDTable(uuid=uuid, name=node['name'])
        en.create()
        
        ##TODO: move uuid to props!
        print 'uuid generated ' +str(uuid) #change this code : TODO

        nayanode =  self.coredb.insertCoreNodeWrap(node, uuid)

        ##at this point the node is inserted in db and neo4j
        ##have to insert changes to index db

        print self.insertToIndexDBHelper(uuid) +' rows added for uuid '+str(uuid)
        return nayanode


    def insertCoreHyperEdgeNodeHelper(self, node):   

        ##a very basic necessity of this! 
        ##as henids and graphs are linked

        ##todo: a table for hyperedgenodes, labels, connected entities
        from app.models.dbmodels.idtables import HyperEdgeNode
        labels  = ''
        for label in node.labels:
            labels = labels + str(label) + ', '
        hen = HyperEdgeNode(labels)
        hen.create()
        henid = hen.henid

        ##TODO: move uuid to props!

        print 'henid generated ' +str(henid) #change this code : TODO

        return self.coredb.insertCoreHyperEdgeNodeWrap(node, henid)


    def insertCoreRelationHelper(self, crawl_rel): 
        ##this relation contains no metadata
        ##but the start and edn nodes contain metadata for uuids against which resolved

        from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID
        start_node_uuid = crawl_rel.start_node[RESOLVEDWITHUUID]
        end_node_uuid = crawl_rel.end_node[RESOLVEDWITHUUID]

        relid = self.coredb.generateNewRELID() 
        print 'relid generated ' +str(relid) #change this code : TODO

        from app.models.dbmodels.relidtable import RELIDTable
        link = RELIDTable(relid, crawl_rel.type, start_node_uuid, end_node_uuid)
        link.create()

        nayarel =  self.coredb.insertCoreRelWrap(crawl_rel, start_node_uuid, end_node_uuid, relid)

        ##now adding the touched entities to index db for solr
        print self.updateIndexDBHelper(start_node_uuid) +' rows added for uuid '+str(start_node_uuid)
        
        print self.updateIndexDBHelper(end_node_uuid) +' rows added for uuid '+str(end_node_uuid)

        return nayarel

    def matchNodesInCore(self, crawl_obj_original):

        
        ##use the crawl object original - and generate search query to get
        ##keywords aliases labels name 
        from app.constants import CRAWL_EN_ID_NAME
        print 'This will be the search query!!!!!!' ##TODO:remove
        name, labels, aliases, keywords = self.crawldb.generateSearchData(CRAWL_EN_ID_NAME, crawl_obj_original[CRAWL_EN_ID_NAME],
            True, getList = True)

        print name
        print aliases
        print labels
        print keywords

        from app.solr.searchsolr_phonetic import get_uuids
        matchingUUIDS = get_uuids(labels=labels, name=name, aliases = aliases, keywords=keywords)
        print  matchingUUIDS

        if len(matchingUUIDS)>50: ##to show first 50 results
            matchingUUIDS = matchingUUIDS[:50]

        ##remove this to have search for you!
        #matchingUUIDS = [154293, 154294]

        return self.coredb.getNodeListCore(matchingUUIDS)

    def matchRelationsInCore(self, crawl_rel):
        '''
            Returns a list of relations that are almost as same as this crawl_rel object from crawldb
        '''    
        from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID
        
        start_node_uuid = crawl_rel.start_node[RESOLVEDWITHUUID]
        end_node_uuid = crawl_rel.end_node[RESOLVEDWITHUUID]

        return self.coredb.searchRelations(start_node_uuid, crawl_rel.type, end_node_uuid)


    def matchHyperEdgeNodesInCore(self, crawl_obj):
        '''
            Returns a list of hyperedge nodes that are almost as same as this crawl_obj object from crawldb
        '''    
        from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID, RESOLVEDWITHHENID

        ens = self.getDirectlyConnectedEntitiesCrawl('hyperedgenode', crawl_obj)

        print ens

        enuuids = []

        for en in ens:
            enuuids.append(en[RESOLVEDWITHUUID])

        return self.coredb.searchHyperEdgeNodes(crawl_obj.labels, enuuids)


    def getTwoVars(self, kind): ##kind is kind of task
        CRAWL_ID_NAME = None ##Property name in crawl graph
        CURR_ID = None ##Session variable

        from app.constants import CRAWL_EN_ID_NAME, CRAWL_REL_ID_NAME, CRAWL_HEN_ID_NAME

        ##TODO: curr_id using getCoreIDName
        
        if kind == 'relation':
            CRAWL_ID_NAME = CRAWL_REL_ID_NAME
            CURR_ID = 'curr_relid'
        elif kind == 'node':
            CURR_ID = 'curr_uuid'
            CRAWL_ID_NAME = CRAWL_EN_ID_NAME
        elif kind == 'hyperedgenode':
            CURR_ID = 'curr_henid'
            CRAWL_ID_NAME = CRAWL_HEN_ID_NAME

        return CRAWL_ID_NAME, CURR_ID


    def areTasksLeft(self, kind): ##kind is kind of task
        
        ans = False

        if kind == 'node':
            ans = self.areCrawlNodesLeft() 
        elif kind=='relation':
            ans = self.areCrawlRelationsLeft()
        elif kind == 'hyperedgenode':
            ans = self.areCrawlHyperEdgeNodesLeft()

        return ans

    def nextTaskToResolve(self, kind, userid):

        '''
            given a kind - node, relation, hyperedge
            calls the appropriate method
            and returns the next graph object to resolve
        '''

        graphobj = None

        if kind == 'relation':
            graphobj =  self.nextRelationToResolve(userid)
        elif kind == 'node':
            graphobj =  self.nextNodeToResolve(userid)
        elif kind == 'hyperedgenode':
            graphobj = self.nextHyperEdgeNodeToResolve(userid) 
        
        return graphobj


    def getCrawlObjectByID(self, kind, id_prop, id_val, isIDString):
        
        '''
            given a crawl_id like _crawl_en_id_ and its value,
            fetches the crawl node from crawldb
        '''

        if kind == 'relation':
            return self.crawldb.getRelationByUniqueID(id_prop, id_val, isIDString)
        elif kind == 'node':
            return self.crawldb.getNodeByUniqueID('entity', id_prop, id_val, isIDString)
        elif kind == 'hyperedgenode':
            return self.crawldb.getNodeByUniqueID('hyperedgenode',id_prop,id_val, isIDString)

        return None


    def copyCrawlObject(self, kind, crawl_obj_original):
        
        '''
            given the kind and the crawl_obj,
            copies the crawl object accrodingly
            node:copies all props, labels and no metadata
            rel: copies all props, label, no relation metadata but meta of connected nodes for identification
        '''

        if kind == 'relation':
            return self.crawldb.copyRelationWithEssentialNodeMeta(crawl_obj_original)
        elif kind == 'node' or kind == 'hyperedgenode':
            return self.crawldb.copyNodeWithoutMeta(crawl_obj_original)

        return None

    def matchPossibleObjects(self, kind, crawl_obj, crawl_obj_original):
        
        '''
            the heart and soul of the verifier task
            the faster this method is the better for the human
            the better this method is the easier for the human
            given a crawl_obj matches those kind of objects in the graph
            and gives possible matches
        '''

        if kind == 'relation':
            return self.matchRelationsInCore(crawl_obj)
        elif kind == 'node':
            return self.matchNodesInCore(crawl_obj_original)
        elif kind == 'hyperedgenode':
            return self.matchHyperEdgeNodesInCore(crawl_obj)

        return None #or an empty list?


    def insertCoreGraphObjectHelper(self, kind, crawl_obj):
        
        '''
            based on the kind, creates the graph object
            inserts it in core graph db,
            and returns the corresponding id - uuid, relid, hyperedgeid
        '''

        if kind=='node':
            curr_obj = self.insertCoreNodeHelper(crawl_obj)
            return curr_obj['uuid']
        elif kind == 'relation':
            curr_obj = self.insertCoreRelationHelper(crawl_obj)
            return curr_obj['relid']
        elif kind == 'hyperedgenode':
            curr_obj = self.insertCoreHyperEdgeNodeHelper(crawl_obj)
            return curr_obj['henid']

        return None

    def setResolvedWithID(self, kind, crawl_obj_original, curr_id):
        '''
            based on kind - node, relation, hyperedge, etc.,
            gives a resolveid to the graphobj of crawldb and sets this
            resolveid to the curr_id that we get from the coredb
        '''
        if kind == 'node':
            self.crawldb.setResolvedWithUUID(crawl_obj_original, curr_id)
        elif kind == 'relation':
            self.crawldb.setResolvedWithRELID(crawl_obj_original, curr_id)
        elif kind == 'hyperedgenode':
            self.crawldb.setResolvedWithHENID(crawl_obj_original, curr_id)
        return
        #doesn't return anything just sets resolved ID

    def getCoreIDName(self, kind):

        ##after seeing all this i think there should have been three class node, link, hyperedgenode and they should have these recurring functions
        ##on which we could directly call these methods
        ##else this is becoming a pain in the neck as the code is growing

        '''
            given a kind, returns the core id name for that graph object
            relid, uuid, hyperedgeid, etc.
        '''

        if kind == 'node':
            return 'uuid'
        elif kind == 'relation':
            return 'relid'
        elif kind == 'hyperedge':
            return 'henid'

        return None

    def getDirectlyConnectedEntitiesCrawl(self, kind, graphobj):

        if kind == 'hyperedgenode':
            from app.constants import CRAWL_HEN_ID_NAME, LABEL_HYPEREDGE_NODE
            return self.crawldb.getDirectlyConnectedEntities(CRAWL_HEN_ID_NAME, graphobj[CRAWL_HEN_ID_NAME], LABEL_HYPEREDGE_NODE, isIDString = True)

        return None

    def getDirectlyConnectedEntitiesCore(self, kind, graphobj):

        if kind == 'hyperedgenode':
            from app.constants import CORE_GRAPH_UUID, LABEL_HYPEREDGE_NODE
            return self.crawldb.getDirectlyConnectedEntities(CORE_GRAPH_UUID, graphobj[CORE_GRAPH_UUID], LABEL_HYPEREDGE_NODE, isIDString = True)

        return None

    def getOriginalCoreObject(self, kind, curr_id):

        orig = None

        if kind == 'relation':
            orig = self.coredb.relation(curr_id)

        elif kind == 'node':
            orig = self.coredb.entity(curr_id)

        elif kind == 'hyperedgenode':
            orig = self.coredb.hyperedgenode(curr_id)

        return orig

    def getNewLabelsAndPropsDiff(self, kind, orig, naya):

        new_labels = None

        if kind == 'node': ##hen can only have two labels thats it!
            new_labels = self.coredb.labelsToBeAdded(orig,naya)

        conf_props,new_props = self.coredb.propsDiff(orig,naya)

        return new_labels, conf_props, new_props

    def checkLockProperties(self, crawl_obj_original, userid):
        if crawl_obj_original.properties.get('_lockedby_') is None:
            return "none" ##locked by none
        if crawl_obj_original.properties.get('_lockedby_') != userid:
            return "other" ##locked by other





         
