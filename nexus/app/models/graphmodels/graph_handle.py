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


         
