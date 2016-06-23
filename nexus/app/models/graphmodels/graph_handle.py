from app.models.graphmodels.graphdb import SelectionAlgoGraphDB, CoreGraphDB
from flask import current_app


class GraphHandle():

    """Business logic for dealing with graph and querying the right graph"""

    def __init__(self):

        self.crawldb = SelectionAlgoGraphDB()

        self.coredb = CoreGraphDB()

    def getWikiNodeStats(self):
        return self.crawldb.getTotalWikiNodeCount(), self.crawldb.getActualWikiNodeCount()

    def getWikiRelationStats(self):
        return self.crawldb.getTotalWikiRelationCount(), self.crawldb.getActualWikiRelationCount()

    def getCrawlNodeStats(self):
        return self.crawldb.countUnresolvedNodes(), self.crawldb.countNotLockedUnresolvedNodes(), self.crawldb.countNextNodesToResolve()

    def getCrawlRelationStats(self):
        n1 = self.crawldb.countUnresolvedRelations()
        n2 = self.crawldb.countLockedRelationsBeingResolved()
        n3 = self.crawldb.countNextRelationsToResolve()
        return  n1, n2, n3

    def getCrawlHyperEdgeNodeStats(self):
        return self.crawldb.countUnresolvedHyperEdgeNodes(), self.crawldb.countNextHyperEdgeNodesToResolve()

    def areCrawlNodesLeft(self):
        n1,n2,n3 = self.getCrawlNodeStats()
        return n2 != 0 ##here the second count will work as we just need to select any node that is not locked

    def areCrawlHyperEdgeNodesLeft(self):
        n1,n2 = self.getCrawlHyperEdgeNodeStats()
        return n1 != 0 ##here the first count can work as we just need to select any hyper edge node

    def areCrawlRelationsLeft(self):
        r1, r2, r3 = self.getCrawlRelationStats()
        return r3 != 0  ##here the second count works as we just need to select any relation for which the nodes are resolved

    def updateCrawlNode(self, node, uuid):
        self.crawldb.setResolvedWithUUID(node, uuid)

    def updateCrawlRelation(self, rel, uuid):
        self.crawldb.setResolvedWithRELID(self, rel, relid)

    def nextNodeToModerate(self, userid):
        node = self.crawldb.getResolvedButNotModeratedNode()
        if node is None:
            return None
        node = self.crawldb.lockObject(node, userid)
        if node is None:
            ##was already locked if goes in this condition
            node = self.nextNodeToModerate(userid)
            return node

        return node

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

    def nextWikiNodeToResolve(self, userid):

        ##TODO: same as nextNodeToResolve, join both code

        node =  self.crawldb.getNextWikiNode()

        print "[nextWikiNodeToResolve: node: %s]" %(node)

        if node is None:
            ##all nodes resolved or locked -  by new changes
            ##no node to resolve
            return node ##returns a type py2neo.Node, can be None

        node = self.crawldb.lockObject(node, userid)

        if node is None:
            ##was already locked if goes in this condition
            node = self.nextWikiNodeToResolve(userid)
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

    def nextWikiRelationToResolve(self, userid):

        ##all theses method nextRelationToResolve, nextNodeToResolve, nextWikiNodeToResolve all seem same
        ##TODO: merge
        rel =  self.crawldb.getNextWikiRelation()
        if rel is None:
            return rel

        rel = self.crawldb.lockObject(rel, userid)
        if rel is None:
            rel = self.nextWikiRelationToResolve(userid)
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

        ## this has been done in views.py for verifier diff push
        ##TODO: move this code to views.py as is the case with diffPushGen
        print self.insertToIndexDBHelper(uuid) +' rows added for uuid '+str(uuid)

        return nayanode

    def provenanceID(self, crawl_obj_original):
        '''
            To be called after crawl_obj_original has been resolved with a core_obj
            To be called after all the verifiedby, verifiedat information saved in crawl_obj_original
            Will fetch all these info from the crawl_obj_original
            And save the info in changeitem table and generate a new change id for this crawl_obj_original
        '''
        # from the crawl_obj get all these vars and insert
        # all this data will be in crawl obj
        # TODO: for all these make changes in API work too!
        # TODO: this should happen only after all these are set in crawldb apis

        from app.constants import CRAWL_PUSHDATE, CRAWL_FETCHDATE, CRAWL_SOURCEURL, CRAWL_VERIFIEDBY, CRAWL_VERIFYDATE, CRAWL_TASKID, CRAWL_PUSHEDBY
        from app.utils.commonutils import Utils
        from app.models.dbmodels.change import ChangeItem
        utils = Utils()


        fetchdate = utils.getDateTimeFromTimestamp( float( crawl_obj_original[CRAWL_FETCHDATE] ) )
        pushdate = utils.getDateTimeFromTimestamp( float ( crawl_obj_original[CRAWL_PUSHDATE] ) )
        verifydate = utils.getDateTimeFromTimestamp( float( crawl_obj_original[CRAWL_VERIFYDATE] ) )
        pushedby = str( crawl_obj_original[CRAWL_PUSHEDBY] )
        verifiedby = str(crawl_obj_original[CRAWL_VERIFIEDBY])
        sourceurl = str(crawl_obj_original[CRAWL_SOURCEURL])
        taskid = crawl_obj_original[CRAWL_TASKID] ##TODO: check in api, if taskid int or not

        chg = ChangeItem(taskid=taskid, pushedby=pushedby, verifiedby=verifiedby, sourceurl=sourceurl, fetchdate=fetchdate, pushdate=pushdate, verifydate = verifydate)
        chg.insert()

        print '[provenanceID: generate new change id for %s id being : %s]' %(crawl_obj_original, str(chg.changeid))

        return chg.changeid



    def provenanceMetaDB(self, kind, new_labels, new_props, conf_props, changeid, curr_id, curr_obj, old_obj):
        '''     Inserts alll metadata in 4 tables for uuidprops, uuidlabels, etc.
                Note: After a lot of thought changetype removed from arguments as
                for new_props and new_labels changetype will be CHANGE_INSERT
                for conf_props will be CHANGE_MODIFY
                Working: This method will fill in the uuidlabels, uuidprops table based on diff provided
                To be called after changeid has been generated
                Idea: Since this is after the object has been inserted in coredb, curr_obj contains latest of everything
                Thats why new_props will be accessed from curr_obj

                But conf_props have old value from old_obj! Phew! Both curr_obj:core and old_obj:core needed for this!
                old_obj None when new graphboject insert

                Note on MVP: since this method is being called when all has been done, so should have no problem
                Example: aliases updated, will detect a change in diff methods and will be updated in next
                Also, a prop is MVP will be able to check from MVP list in future: dont complicate
        '''

        numrows = 0

        ##step1: check if all empty list or None
        flag = True
        if (new_labels is None or new_labels == []):
            if (new_props is None or new_props == []):
                if (conf_props is None or conf_props == []):
                    flag = False

        if not flag:
            return numrows ##returns 0

        # Ofcourse there should be a curr_obj : core_obj
        from app.constants import CHANGE_INSERT, CHANGE_MODIFY, MVPLIST
        from app.utils.commonutils import Utils

        ##step 2 : generate a change id for this
        ##done in provenanceID: so changeid is in arguments

        if kind=='node':
            from app.models.dbmodels.uuid import UuidLabels, UuidProps
            for label in new_labels:
                newlabel = UuidLabels(changeid=changeid, uuid=curr_id, label=label, changetype=CHANGE_INSERT)
                newlabel.create() ##TODO: check when execute returns numrows
                numrows = numrows + 1
                ##TODO: I think that UuidLabels etc. should have an auto inc column to kepe track if inserted or not
            for prop in new_props:
                ##TODO: almost similar code for relation and nodes, get together
                curr_obj_val = curr_obj[prop]
                if prop in MVPLIST or type(curr_obj[prop]) is list:
                    curr_obj_val = Utils.convertToRegularList(curr_obj_val)
                newitem = UuidProps(changeid=changeid, uuid=curr_id, propname=prop, changetype=CHANGE_INSERT, newpropvalue=str(curr_obj_val))
                newitem.create()
                numrows = numrows + 1
            for prop in conf_props: ##for fresh insert wont go inside
                curr_obj_val = curr_obj[prop]
                old_obj_val = old_obj[prop]
                olditem = UuidProps(changeid=changeid, uuid=curr_id, propname=prop, changetype=CHANGE_MODIFY, oldpropvalue = str(old_obj_val), newpropvalue=str(curr_obj_val))
                olditem.create()
                numrows = numrows + 1
        elif kind=='relation':
            from app.models.dbmodels.relid import RelLabels, RelProps
            for label in new_labels:
                newlabel = RelLabels(changeid=changeid, relid=curr_id, label=label, changetype=CHANGE_INSERT)
                newlabel.create()
                numrows = numrows + 1
                ##TODO: I think that UuidLabels etc. should have an auto inc column to kepe track if inserted or not
            for prop in new_props:
                curr_obj_val = curr_obj[prop]
                if prop in MVPLIST or type(curr_obj[prop]) is list:
                    curr_obj_val = Utils.convertToRegularList(curr_obj_val)
                newitem = RelProps(changeid=changeid, relid=curr_id, propname=prop, changetype=CHANGE_INSERT, newpropvalue=str(curr_obj_val))
                newitem.create()
                numrows = numrows + 1
            for prop in conf_props:
                curr_obj_val = curr_obj[prop]
                old_obj_val = old_obj[prop]
                # if prop in MVPLIST or type(curr_obj[prop]) is list or type(old_obj[prop]) is list:
                #     ##TODO: test for MVP in relations
                #     curr_obj_val = Utils.convertToRegularList(curr_obj_val)
                #     old_obj_val = Utils.convertToRegularList(old_obj_val)
                olditem = RelProps(changeid=changeid, relid=curr_id, propname=prop, changetype=CHANGE_MODIFY, oldpropvalue = str(old_obj_val), newpropvalue=str(curr_obj_val))
                ##IDEA: TODO: Now I am thinking instead of all this mysql hoopla
                ## the original idea of versioning each node in a separate graph would have been the best!
                ## why? every type is string here but in neo4j it has different types!
                ## same issue with api when pushing data
                olditem.create()
                numrows = numrows + 1
        return numrows ##won't reach here

    def provenanceCore(self, old_obj, curr_obj, curr_id, crawl_obj_original, kind):
        '''
            To be called after all resolution and updation done.
            Needless to say all old_obj, curr_obj, crawl_obj_original are of same kind.
            Uses two helper methods provenanceID and provenanceMetaDB
        '''
        # TODO:I think unlock should happen here and nowhere else from now on!

        # get change id also -- step 1
        # after this changeitem will be inserted with taskid and everything
        changeid = self.provenanceID(crawl_obj_original=crawl_obj_original)

        ##get the object items to update
        ##step- get new diff: old is None as insert
        new_labels, conf_props, new_props = self.coredb.compareTwoObjects(old_obj, curr_obj, kind)

        #step: insert one by one in meta db
        numrows = self.provenanceMetaDB(kind, new_labels, new_props, conf_props, changeid, curr_id, curr_obj, old_obj)
        return changeid, numrows

    def resolveAndProvenance(self, kind, curr_id, curr_obj, old_obj, crawl_obj_original, verifiedby):
        '''
            if old_obj and curr_obj both None, then resolve fast
            old_obj can be None if only insertion
            curr_obj can not be None - but if it is fast resolve
        '''
        changeid = None
        numrows = None

        ##Provenance patch
        ##DONE: set resolved and also other props here, verified by, verified at, etc.
        self.setResolvedWithID(kind, crawl_obj_original, curr_id, verifiedby)

        if curr_obj is not None: # not fast resolve
            changeid, numrows = self.provenanceCore(old_obj, curr_obj, curr_id, crawl_obj_original, kind)

        ##only after all the resolution complete and done
        self.crawldb.unlockObject(crawl_obj_original)

        return changeid, numrows


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
        ##yes when the relation is inserted!!
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

    def getIDForKind():
        pass

    def getAllVars(self):
        kinds = ['node','relation']
        ret = []
        for kind in kinds:
            a,b = self.getTwoVars(kind)
            ret.append((a,kind))
            ret.append((b,kind))
        return ret

    def areCrawlTasksLeft(self, kind):

        ans = False

        if kind == 'node':
            ans = self.areCrawlNodesLeft()
        elif kind=='relation':
            ans = self.areCrawlRelationsLeft()
        elif kind == 'hyperedgenode':
            ans = self.areCrawlHyperEdgeNodesLeft()

        return ans

    def areWikiTasksLeft(self, kind):
        if kind == 'node':
            n1,n2 =  self.getWikiNodeStats()
            return n2!=0
        elif kind == 'relation':
            r1, r2 = self.getWikiRelationStats()
            return r2!=0

        print "[areWikiTasksLeft: ERROR: should not reach here]"
        return False

    def areTasksLeft(self, kind, tasktype): ##kind is kind of task

        if tasktype=='crawl':
            return self.areCrawlTasksLeft(kind)
        elif tasktype == 'wiki':
            return self.areWikiTasksLeft(kind)

        print "[areWTasksLeft: ERROR: should not reach here]"
        return False


    def nextCrawlTaskToResolve(self, kind, userid):
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

    def nextWikiTaskToResolve(self, kind, userid):
        '''
            given a kind - node, relation, hyperedge
            calls the appropriate method
            and returns the next graph object to resolve
        '''

        graphobj = None

        if kind == 'node':
            graphobj =  self.nextWikiNodeToResolve(userid)
        elif kind == 'relation':
            graphobj =  self.nextWikiRelationToResolve(userid)

        return graphobj

    def nextTaskToResolve(self, kind, tasktype, userid):

        '''
            appendum: added tasktype too to have similar flow
            given a kind - node, relation, hyperedge
            calls the appropriate method
            and returns the next graph object to resolve
        '''

        if tasktype == 'crawl':
            return self.nextCrawlTaskToResolve(kind, userid)
        elif tasktype == 'wiki':
            return self.nextWikiTaskToResolve(kind, userid)

        return None

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
        curr_obj = None
        retid = None

        if kind=='node':
            curr_obj = self.insertCoreNodeHelper(crawl_obj)
            retid =  curr_obj['uuid']
        elif kind == 'relation':
            curr_obj = self.insertCoreRelationHelper(crawl_obj)
            retid =  curr_obj['relid']
        elif kind == 'hyperedgenode':
            curr_obj = self.insertCoreHyperEdgeNodeHelper(crawl_obj)
            retid =  curr_obj['henid']

        return retid

    def setResolvedWithID(self, kind, crawl_obj_original, curr_id, verifiedby):
        '''
            based on kind - node, relation, hyperedge, etc.,
            gives a resolveid to the graphobj of crawldb and sets this
            resolveid to the curr_id that we get from the coredb
        '''
        if kind == 'node':
            self.crawldb.setResolvedWithUUID(crawl_obj_original, curr_id, verifiedby)
        elif kind == 'relation':
            self.crawldb.setResolvedWithRELID(crawl_obj_original, curr_id, verifiedby)
        # elif kind == 'hyperedgenode':
        #     self.crawldb.setResolvedWithHENID(crawl_obj_original, curr_id)
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

        new_labels = []

        if kind == 'node': ##hen can only have two labels thats it!
            new_labels = self.coredb.labelsToBeAdded(orig,naya)

        conf_props,new_props = self.coredb.propsDiff(orig,naya)

        return new_labels, conf_props, new_props

    def checkLockProperties(self, crawl_obj_original, userid):

        if crawl_obj_original.properties.get('_lockedby_') is None:
            lockprop = "none"
            msg = "Graph object's lock aready been removed. Begin again "

        elif crawl_obj_original.properties.get('_lockedby_') != userid:
            lockprop =  "other" ##locked by other
            msg = "Graph object's lock is with someone else. Begin again "

        else:
            lockprop = "allowed"
            msg = "Graph object's lock is not with you. Begin again "

        return lockprop, msg

    def wikiObjectCreateHelper(self, kind, obj, userid, sourceurl):
        '''
            Note: works directly on obj, has been used like that
            working directly on the given object as
            assumption that the object is already not bound and copied
            Just changes the object, doesn't create/update
        '''

        from app.utils.commonutils import Utils
        from app.constants import CRAWL_TASKID, CRAWL_PUSHDATE, CRAWL_PUSHEDBY, CRAWL_TASKTYPE
        from app.constants import CRAWL_SOURCEURL, CRAWL_FETCHDATE, CRAWL_EN_ID_NAME, CRAWL_REL_ID_NAME, RESOLVEDWITHUUID, RESOLVEDWITHRELID
        from app.constants import CRAWL_NODENUMBER, CRAWL_RELNUMBER, CRAWL_EN_ID_FORMAT, CRAWL_REL_ID_FORMAT

        ##common for both kinds of objects
        ID_NAME = self.getCoreIDName(kind)
        curr_id = obj[ID_NAME]
        obj[ID_NAME] = None

        from app.models.dbmodels.tasks import Tasks
        task = Tasks.getWikiTaskByUser(userid)
        ##will throw an error if not in db, it will be our problem, not anybody's - would only occur if the at time of user creation, entry not updated here
        obj[CRAWL_TASKID] =  task.taskid##get from db for thi user

        if kind=='node':
            obj[RESOLVEDWITHUUID] = curr_id
            obj[CRAWL_NODENUMBER] = int(Utils.currentTimeStamp()) ##though idiotic, we wont be needing it for this!
            obj[CRAWL_EN_ID_NAME] = CRAWL_EN_ID_FORMAT %(obj[CRAWL_TASKID], obj[CRAWL_NODENUMBER])
        elif kind=='relation':
            obj[RESOLVEDWITHRELID] = curr_id
            obj[CRAWL_RELNUMBER] = int(Utils.currentTimeStamp())
            obj[CRAWL_REL_ID_NAME] = CRAWL_REL_ID_FORMAT %(obj[CRAWL_TASKID], obj[CRAWL_RELNUMBER])

        obj[CRAWL_PUSHEDBY] = userid
        obj[CRAWL_PUSHDATE] = Utils.currentTimeStamp()


        obj[CRAWL_SOURCEURL] = sourceurl
        obj[CRAWL_FETCHDATE] = obj[CRAWL_PUSHDATE] ##since wiki work! dates same!
        obj[CRAWL_TASKTYPE] = "wiki"

        return obj,curr_id

    def wikiObjCreate(self, kind, obj, userid, sourceurl):
        '''
            would be a wrapper for a node, a dummy object
            not bound to any graph - crawldb or coredb
            validate the obj for prop and label error before sending here
        '''

        obj,curr_id = self.wikiObjectCreateHelper(kind,obj,userid,sourceurl)


        if kind=='relation':

            start_node,start_id = self.wikiObjectCreateHelper('node',obj.start_node,userid,sourceurl)

            end_node, end_id = self.wikiObjectCreateHelper('node',obj.end_node,userid,sourceurl)

        self.crawldb.graph.create(obj)
        ##first will have to create to use setResolvedWithID

        if kind=='relation':

            self.setResolvedWithID('node',obj.start_node,start_id,'nexusbot')

            self.setResolvedWithID('node',obj.end_node,end_id,'nexusbot')

        # print str(obj.end_node)

        ##Decided not doing:  diff and check and use that only with labels intact
        ##if prop not in conf_props or new_props use it else set to None for us
        ##this will be automatically handled by diff btw!

        # self.crawldb.graph.create(obj)

        # copyobj = self.getCrawlObjectByID('node',CRAWL_EN_ID_NAME,obj[CRAWL_EN_ID_NAME],True)

        #flash(copyobj)
        return obj
