from app.verifier import verifier
from flask import render_template, flash, redirect, session, request, url_for, current_app
from app.models.graphmodels.graph_handle import GraphHandle

@verifier.route('/')
def show():
    # have a verifier page!
    # show the begin task button!
    gg = GraphHandle()
    unresolvedTotal, immediateUnResolvedTotal = gg.getCrawlNodeStats()
    r_unresolvedTotal, r_immediateUnResolvedTotal = gg.getCrawlRelationStats()
    return render_template("verifier_home.html", homeclass="active",unresolvedTotal = unresolvedTotal, immediateUnResolvedTotal = immediateUnResolvedTotal, r_unresolvedTotal = r_unresolvedTotal, r_immediateUnResolvedTotal = r_immediateUnResolvedTotal)


@verifier.route('/startNodeTask/')
def startNodeTask():

    CRAWL_EN_ID_NAME = current_app.config['CRAWL_EN_ID_NAME'] ##TODO: move to a constant file?
    CURR_UUID = 'curr_uuid' ##TODO: move somehwre?

    ##TODO: remove when not needed!
    session.pop(CRAWL_EN_ID_NAME, None)
    session.pop(CURR_UUID, None)

    ##TODO: check if four vars exist in session directly redirect to runTask
    #temptext = ''
    ##or may be invalidate all 4 vars on this and restart! the task id! TODO!
    if session.get(CRAWL_EN_ID_NAME) is not None:
        print 'startTask: in the middle of a node resolution task for node : '+str(session.get(CRAWL_EN_ID_NAME))  
        return redirect(url_for('.matchNodeNew')) ##changed here!

    gg = GraphHandle()

    if gg.areCrawlNodesLeft(): ##if task exists in crawl db!
        
        print 'startTask: ckecked task exists!!'

        node = gg.nextNodeToResolve()
        print 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
        print node

        session[CRAWL_EN_ID_NAME] = node[CRAWL_EN_ID_NAME]

        print '\n\nstartTask: Beginning resolution for node with crawl id: '+node[CRAWL_EN_ID_NAME]+'\n\n'


        print 'startTask: now redirecting'

        return redirect(url_for('.matchNodeNew'))
        

    else:

        temptext = 'No pending tasks'
    
    return render_template("temp.html", homeclass="active", 
        temptext=temptext)


##TODO: shoudlnt the number be in form or something??
@verifier.route('/matchNodeNew/',methods=["GET","POST"])
def matchNodeNew():

    CRAWL_EN_ID_NAME = current_app.config['CRAWL_EN_ID_NAME']
    CURR_UUID = 'curr_uuid'

    if session.get(CRAWL_EN_ID_NAME) is None:
        return redirect(url_for('.show'))

    gg = GraphHandle()
    crawl_node_original = gg.crawldb.getNodeByUniqueID(CRAWL_EN_ID_NAME, session[CRAWL_EN_ID_NAME], isIDString=True)
    crawl_node = gg.crawldb.copyNodeWithoutMeta(crawl_node_original) 

    ##TODO: validation as well! 

    if not request.form:

        matchingUUIDS = [569]

        ##use apache solr code here
        ##from app.resolver import *      
        ##print resolveNode('xx') ##TODO: remove this!
        ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
    
        graphnodes = gg.coredb.getNodeListCore(matchingUUIDS)     

        return render_template("verifier_match_node.html", homeclass="active",
            row=crawl_node, graphnodes=graphnodes, nodeID = session[CRAWL_EN_ID_NAME])
    else:

        ##get the matched_uuid! save it in sessnio or where-ever you want
        #print request.form['match_uuid']

        flash(request.form['match_uuid'])

        if request.form['match_uuid']!='##NA##':            
            session[CURR_UUID] = request.form['match_uuid']
            return redirect(url_for('.diffPushGen', kind = 'node'))

        else:


            ##assuming the curr_node has name property if not. no way are we going to isert it! ##TODO a check!!!
            ##create
            curr_node = gg.coredb.insertCoreNodeWrap(crawl_node)
            curr_uuid = curr_node['uuid']

            flash('Node created with uuid: '+ str(curr_node['uuid']))
            flash(CRAWL_EN_ID_NAME +str(session[CRAWL_EN_ID_NAME]))

            ##pop session objects
            session.pop(CRAWL_EN_ID_NAME, None)
            session.pop(CURR_UUID, None) ##redundant code!

            ##updateResolved PART
            gg.crawldb.setResolvedWithUUID(crawl_node_original, curr_uuid) ##change to original
            
            #return render_template("temp.html", homeclass="active",temptext="NEW NODE CREATED DONE!")
            return redirect(url_for('.show'))
            ##TODO: second return


            #MAJOR TODO: 


        ##pop session.curr_number here


        

    # ## TODO!!
    # ## form showing all matched uuids
    # ## fetch one uuid from the form
    # ## let uuid = 25 for '1' and 28 for '2' for sake of simplicity here
    # ## forward to diffPush method with number and uuid

    # ##handle the case when no uuid is resturned TODO!
    # ##just create a new node in above case
    # session['curr_number'] = number ##popping out ?? TODO!
    # if number=='1':
    #     session['curr_uuid'] = 25
    # else:
    #     session['curr_uuid'] = 28

    # ##g is creating a lot of problems but why!!
    # ##have to use session for such a thing! bad! TODO! check what is the solution!

    # return redirect(url_for('.diffPush'))
    

##two params: number and uuid ?? in session!
@verifier.route('/diffPush/', methods=["GET","POST"])
def diffPush():

    CRAWL_EN_ID_NAME = current_app.config['CRAWL_EN_ID_NAME']
    CURR_UUID = 'curr_uuid'

    if session.get(CURR_UUID) is None:
        return render_template("temp.html", homeclass="active", temptext='No diff tasks go to start task/match task first!')

    gg = GraphHandle()

    curr_uuid = session.get(CURR_UUID)
    crawl_en_id = session.get(CRAWL_EN_ID_NAME)
    crawl_node_original = gg.crawldb.getNodeByUniqueID(CRAWL_EN_ID_NAME, session[CRAWL_EN_ID_NAME], isIDString = True)
    crawl_node = gg.crawldb.copyNodeWithoutMeta(crawl_node_original) 
   

    orig = gg.coredb.entity(curr_uuid)##from the graph
    naya = crawl_node ##from the row

    orig.pull()
    #naya.pull() ##wont work now as naya node is not bound now
    ##print 'orig: ' + str(orig)
    ##print '-------'
    ##print 'naya: ' + str(naya)
    ##print '-------'

    new_labels = gg.coredb.labelsToBeAdded(orig,naya) 
    conf_props,new_props = gg.coredb.propsDiff(orig,naya)

    if not request.form:

        return render_template("verifier_diff_node.html", homeclass="active",
            new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya, crawl_en_id = session[CRAWL_EN_ID_NAME])
    else:

        
        for prop in conf_props:
            flash(prop+' : '+request.form[prop])
            ##update this prop in orig node!
            #orig[prop] = request.form[prop]
            orig[prop] = request.form[prop] ##naya prop/orig prop 

        
        for label in request.form.getlist('newlabels'):
            flash('Label: '+str(label))
            ##add this label to orig!
            orig.labels.add(label)

        
        for prop in new_props:
            value_list = request.form.getlist(prop)
            if len(value_list)==1: ##as only one value is going to be any way!
                flash(prop+' : '+str(value_list[0]))
                ##add this prop to orig node!
                #orig[prop] = request.form[prop]
                orig[prop] = request.form[prop] ##naya prop/orig prop 
        
        ##print orig  
        ##now can push! TODO!
        

        orig.push()#3one node resolved! 

        
        flash(CRAWL_EN_ID_NAME+str(session[CRAWL_EN_ID_NAME]))

        gg.crawldb.setResolvedWithUUID(crawl_node_original, curr_uuid)

        ##pop session objects
        session.pop(CRAWL_EN_ID_NAME, None)
        session.pop(CURR_UUID, None) ##redundant code!
        
        return redirect(url_for('.show'))


        #return render_template("temp.html", homeclass="active",temptext="DIFF DONE!")



    # #uuid = request.args.get('uuid') ##not working at all since immutable
    # #push something to this uuid here!

    # ##some mechanism will give us a new py2neo node ---> after the selection of the diffs, based on labels, props, etc.
    # ##we will write a method to push that new py2neo node if uuid exists!

    # ##TODO: show a start task button here
    # return render_template("temp.html", homeclass="active", 
    #     temptext='Push something new to '+ str(uuid)+' task completed') ##str beacuse of None

    ##TODO: same validation checks like _ for wiki thing too 



@verifier.route('/startRelTask/')
def startRelTask():

    from app.constants import CRAWL_REL_ID_NAME
    CURR_RELID = 'curr_relid' ##TODO: move somehwre?

    ##TODO: remove when not needed!
    session.pop(CRAWL_REL_ID_NAME, None)
    session.pop(CURR_RELID, None)

    ##TODO: check if session vars exist in session directly redirect to runTask
    if session.get(CRAWL_REL_ID_NAME) is not None:
        print 'startRelTask: in the middle of a relation resolution task for relation : '+str(session.get(CRAWL_REL_ID_NAME))  
        return redirect(url_for('.matchRelNew')) ##changed here!

    gg = GraphHandle()

    if gg.areCrawlRelationsLeft(): ##if task exists in crawl db!
        
        print 'startRelTask: ckecked relations to resolve exists!!'

        rel = gg.nextRelationToResolve()
        print rel

        session[CRAWL_REL_ID_NAME] = rel[CRAWL_REL_ID_NAME]

        print '\n\nstartRelTask: Beginning resolution for relation with crawl id: '+rel[CRAWL_REL_ID_NAME]+'\n\n'


        print 'startRelTask: now redirecting'

        return redirect(url_for('.matchRelNew'))
        

    else:

        temptext = 'No pending relations to resolve, sorry'
    
    return render_template("temp.html", homeclass="active", 
        temptext=temptext)



@verifier.route('/matchRelNew/',methods=["GET","POST"])
def matchRelNew():

    from app.constants import CRAWL_REL_ID_NAME
    kind = 'relation'
    CRAWL_ID_NAME = CRAWL_REL_ID_NAME
    CURR_ID = 'curr_relid'
    ##match_uuid. match_relid in different varoables!? TODO

    if session.get(CRAWL_ID_NAME) is None:
        return redirect(url_for('.show'))

    gg = GraphHandle()
    crawl_obj_original = gg.crawldb.getRelationByUniqueID(CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)
    ##essential node meta is required when actually creating the node
    ##also will be required when resolving the relation, though can be taken from original
    crawl_obj = gg.crawldb.copyRelationWithEssentialNodeMeta(crawl_obj_original)
    

    ##TODO: validation as well! 

    if not request.form:

        matchingIDS = [1001]

        ##use apache solr code here
        ##from app.resolver import *      
        ##print resolveNode('xx') ##TODO: remove this!
        ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
    
        graphobjs = gg.coredb.getRelListCore(matchingIDS) 
        print 'reeeeeeeeeeeeeeeeeeeeeeeeeeeeel'
        print graphobjs    

        return render_template("verifier_match_rel.html", homeclass="active",
            row=crawl_obj, graphobjs=graphobjs, ID = session[CRAWL_ID_NAME], kind = kind)
    else:

        ##get the matched_uuid! save it in sessnio or where-ever you want
        #print request.form['match_uuid']

        flash(request.form['match_relid'])

        if request.form['match_relid']!='##NA##':            
            session[CURR_ID] = request.form['match_relid']
            return redirect(url_for('.diffPushGen', kind = 'relation'))

        else:


            ## assuming the curr_relation has a label atleast else no way are we going to isert it! ##TODO a check!!! Can be done at api time too!
            ## create
            ## crawl_obj is the copied object
            curr_obj = gg.coredb.insertCrawledRelationToCore(crawl_obj)
            curr_id = curr_obj['relid'] ##move outside

            flash('Graph object created with id: '+ str(curr_obj['relid']))
            flash(kind+ ' : '+CRAWL_ID_NAME +' : '+str(session[CRAWL_ID_NAME]))

            ##pop session objects
            session.pop(CRAWL_ID_NAME, None)
            session.pop(CURR_ID, None) ##redundant code!

            ##updateResolved PART
            gg.crawldb.setResolvedWithRELID(crawl_obj_original, curr_id)
            #change to original            
            #return render_template("temp.html", homeclass="active",temptext="NEW NODE CREATED DONE!")
            return redirect(url_for('.show'))
            ##TODO: second return


##two params: number and uuid ?? in session!
@verifier.route('/diffPushGen/<string:kind>', methods=["GET","POST"])
def diffPushGen(kind='node'):



    CRAWL_ID_NAME = None ##Property name in crawl graph
    CURR_ID = None ##Session variable

    from app.constants import CRAWL_EN_ID_NAME, CRAWL_REL_ID_NAME
    
    if kind == 'relation':
        CRAWL_ID_NAME = CRAWL_REL_ID_NAME
        CURR_ID = 'curr_relid'
    elif kind == 'node':
        CURR_ID = 'curr_uuid'
        CRAWL_ID_NAME = CRAWL_EN_ID_NAME
    else:
        return 'kind not defined now', 404 

    
    if session.get(CURR_ID) is None:
        return render_template("temp.html", homeclass="active", temptext='No diff tasks go to start task/match task first!')

    gg = GraphHandle()

    curr_id = session.get(CURR_ID)
    crawl_id = session.get(CRAWL_ID_NAME)

    crawl_obj_original = None
    crawl_obj = None
    
    if kind == 'relation':
        crawl_obj_original = gg.crawldb.getRelationByUniqueID(CRAWL_ID_NAME, crawl_id, isIDString = True)
        crawl_obj = gg.crawldb.copyRelationWithEssentialNodeMeta(crawl_obj_original)
        orig = gg.coredb.relation(curr_id)

    elif kind == 'node':
        crawl_obj_original = gg.crawldb.getNodeByUniqueID(CRAWL_ID_NAME, crawl_id, isIDString = True)
        crawl_obj = gg.crawldb.copyNodeWithoutMeta(crawl_obj_original) 
        orig = gg.coredb.entity(curr_id)


    naya = crawl_obj ##from the row

    orig.pull()

    #naya.pull() ##wont work now as naya node is not bound now
    ##print 'orig: ' + str(orig)
    ##print '-------'
    ##print 'naya: ' + str(naya)
    ##print '-------'

    new_labels = None
    if kind == 'node':
        new_labels = gg.coredb.labelsToBeAdded(orig,naya) 
    conf_props,new_props = gg.coredb.propsDiff(orig,naya)

    if not request.form:

        return render_template("verifier_diff_gen.html", homeclass="active",
            new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya, crawl_id = session[CRAWL_ID_NAME], kind=kind)
    else:

        
        for prop in conf_props:
            flash(prop+' : '+request.form[prop])
            ##update this prop in orig graph object!
            #orig[prop] = request.form[prop]
            orig[prop] = request.form[prop] ##naya prop/orig prop 

        
        for label in request.form.getlist('newlabels'):
            flash('Label: '+str(label))
            ##add this label to orig!
            orig.labels.add(label)

        
        for prop in new_props:
            value_list = request.form.getlist(prop)
            if len(value_list)==1: ##as only one value is going to be any way!
                flash(prop+' : '+str(value_list[0]))
                ##add this prop to orig graph object!
                #orig[prop] = request.form[prop]
                orig[prop] = request.form[prop] ##naya prop/orig prop 
        
        ##print orig  
        ##now can push! TODO!
        

        orig.push()#3one node resolved! 

        
        flash(kind+ ' : '+CRAWL_ID_NAME+' : '+ str(session[CRAWL_ID_NAME]))

        if kind == 'relation':
            gg.crawldb.setResolvedWithRELID(crawl_obj_original, curr_id)
        elif kind == 'node':
            gg.crawldb.setResolvedWithUUID(crawl_obj_original, curr_id)

        ##pop session objects
        session.pop(CRAWL_ID_NAME, None)
        session.pop(CURR_ID, None) ##redundant code!
        
        return redirect(url_for('.show'))

