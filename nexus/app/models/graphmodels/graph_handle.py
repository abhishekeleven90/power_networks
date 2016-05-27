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

    def areCrawlNodesLeft(self):
        n1,n2 = self.getCrawlNodeStats()
        return n1 != 0 ##here the first count can work as we just need to select any node

    def areCrawlRelationsLeft(self):
        r1,r2 = self.getCrawlRelationStats()
        return r2 != 0  ##here the second count works as we just need to select any relation for which the nodes are resolved

    def updateCrawlNode(self, node, uuid):
        self.crawldb.setResolvedWithUUID(node, uuid)

    def updateCrawlRelation(self, rel, uuid):
        self.crawldb.setResolvedWithRELID(self, rel, relid)

    def nextNodeToResolve(self):
        #TODO: remove prints
        print self.crawldb
        print 'graph object'
        print self.crawldb.graph
        node, degree =  self.crawldb.getNearestBestNode()
        node2, degree2 =  self.crawldb.getHighestDegreeNode()
        print 'node'
        print node
        return node ##returns a type py2neo.Node, can be None

    def nextRelationToResolve(self):
        rel =  self.crawldb.getNextRelationToResolve()
        return rel ##returns a type py2neo.relation, can be None

    def getNodeListCore(self, uuidList):
        return self.coredb.getListOfNodes(uuidList)

    def insertCoreNodeHelper(self, node):

        ##a very basic necessity of this! 
        ##as uuids and graphs are linked

        from app.models.dbmodels.idtables import Entity
        en = Entity(node['name'])
        en.create()
        uuid = en.uuid

        ##TODO: move uuid to props!
        print 'uuid generated ' +str(uuid) #change this code : TODO

        return self.coredb.insertCoreNodeWrap(node, uuid)


    def insertCoreRelationHelper(self, crawl_rel): 
        ##this relation contains no metadata
        ##but the start and edn nodes contain metadata for uuids against which resolved

        from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID
        
        start_node_uuid = crawl_rel.start_node[RESOLVEDWITHUUID]
        end_node_uuid = crawl_rel.end_node[RESOLVEDWITHUUID]

        from app.models.dbmodels.idtables import Link
        link = Link(crawl_rel.type, start_node_uuid, end_node_uuid)
        link.create()
        relid = link.relid
        print '#### inside @@@@@@ relid - means db working fine '+str(relid)

        return self.coredb.insertCoreRelWrap(crawl_rel, start_node_uuid, end_node_uuid, relid)


    def matchRelationsInCore(self, crawl_rel):
        '''
            Returns a list of relations that are almost as same as this crawl_rel object from crawldb
        '''    
        from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID
        
        start_node_uuid = crawl_rel.start_node[RESOLVEDWITHUUID]
        end_node_uuid = crawl_rel.end_node[RESOLVEDWITHUUID]

        return self.coredb.searchRelations(start_node_uuid, crawl_rel.type, end_node_uuid)

        



         
