from app.graphdbnew import SelectionAlgoGraphDB, CoreGraphDB
from flask import current_app


class GraphHandle():
    
    """Business logic for dealing with graph and querying the right graph"""

    def __init__(self):
        
        self.crawldb = SelectionAlgoGraphDB(username = current_app.config['CRAWL_DB_USER'], password = current_app.config['CRAWL_DB_PASSWORD'], server = current_app.config['CRAWL_DB_HOST'], port = current_app.config['CRAWL_DB_PORT'])

        self.coredb = CoreGraphDB(username = current_app.config['CORE_DB_USER'], password = current_app.config['CORE_DB_PASSWORD'], server = current_app.config['CORE_DB_HOST'], port = current_app.config['CORE_DB_PORT'])

    def getCrawlNodeStats(self):
        return self.crawldb.countUnresolvedNodes(), self.crawldb.countNextNodesToResolve()

    def getCrawlRelationStats(self):
        return self.crawldb.countUnresolvedRelations(), self.crawldb.countNextRelationsToResolve()

    def areCrawlNodesLeft(self):
        n1,n2 = self.getCrawlNodeStats()
        return n1 != 0 ##here the first count can work as we just need to select any node

    def areCrawlRelationsLeft(self):
        r1,r2 = self.getRelationStats()
        return r2 != 0  ##here the second count works as we just need to select any relation for which the nodes are resolved

    def updateCrawlNode(self, node, uuid):
        self.crawldb.setResolvedWithUUID(node, uuid)

    def updateCrawlRelation(self, rel, uuid):
        self.crawldb.setResolvedWithRELID(self, rel, relid)

    def nextNodeToResolve(self):
        print 'inside method'
        print 'object'
        print self.crawldb
        print 'conf'
        print current_app.config['CRAWL_DB_USER']
        print current_app.config['CRAWL_DB_PORT']
        print current_app.config['CRAWL_DB_HOST']
        print current_app.config['CRAWL_DB_PASSWORD']
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

    
class FlowHandle:
    
    def __init__(self):
        pass

    def next(self):
        pass

    def update(self):
        pass
