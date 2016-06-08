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
    h_unresolvedTotal, h_immediateUnResolvedTotal = gg.getCrawlHyperEdgeNodeStats()
    return render_template("verifier_home.html", homeclass="active",
        unresolvedTotal = unresolvedTotal, immediateUnResolvedTotal = immediateUnResolvedTotal, 
        r_unresolvedTotal = r_unresolvedTotal, r_immediateUnResolvedTotal = r_immediateUnResolvedTotal,
        h_unresolvedTotal = h_unresolvedTotal, h_immediateUnResolvedTotal = h_immediateUnResolvedTotal)


@verifier.route('/startTask/<string:kind>/')
def startTask(kind='node'):

    gg = GraphHandle()

    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    ##This is needed whenever a new task is started
    ##Task would mean anything node resolution, rel resolution, or hyperedge resolution
    session.pop(CRAWL_ID_NAME, None)
    session.pop(CURR_ID, None)

    ##TODO: check if session vars exist in session directly redirect to runTask
    if session.get(CRAWL_ID_NAME) is not None:
        print 'startTask: in the middle of a resolution task of kind '+kind+' for graph object : '+str(session.get(CRAWL_ID_NAME))  
        return redirect(url_for('.match', kind = kind)) 

    if gg.areTasksLeft(kind): ##if task exists in crawl db!
        
        print 'startTask: ckecked tasks to resolve exist for kind'+kind+'!!'

        graphobj = gg.nextTaskToResolve(kind)

        print graphobj

        session[CRAWL_ID_NAME] = graphobj[CRAWL_ID_NAME]

        print '\n\nstartTask: Beginning resolution for graph obj with crawl id: '+graphobj[CRAWL_ID_NAME]+'\n\n'
        print 'startTask: now redirecting'

        return redirect(url_for('.match', kind = kind))
        
    ##if the above if doesnt work, comes here
    temptext = 'No pending graph objects of kind '+kind+' to resolve, please go back'
    return render_template("temp.html", homeclass="active", 
        temptext=temptext)


@verifier.route('/match/<string:kind>/',methods=["GET","POST"])
def match(kind='node'):

    gg = GraphHandle()
    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    if session.get(CRAWL_ID_NAME) is None:
        return redirect(url_for('.show'))

    crawl_obj_original = gg.getCrawlObjectByID(kind, CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)

    ##essential node meta is required when actually creating the node
    ##also will be required when resolving the relation, though can be taken from original

    crawl_obj = gg.copyCrawlObject(kind, crawl_obj_original)
    

    ##TODO: validation as well! What actually? I forgot!

    if not request.form:

        graphobjs = gg.matchPossibleObjects(kind, crawl_obj, crawl_obj_original)
        connected_ens = gg.getDirectlyConnectedEntitiesCrawl(kind, crawl_obj_original) ##will be none if not hyperedgenode for now

        return render_template("verifier_match.html", homeclass="active",
            row=crawl_obj, graphobjs=graphobjs, ID = session[CRAWL_ID_NAME], kind = kind, 
            idname = gg.getCoreIDName(kind), connected_ens = connected_ens)
    else:

        ##TODO: change this name in html file
        flash(request.form['match_id']) 

        if request.form['match_id']!='##NA##':            
            session[CURR_ID] = request.form['match_id']
            return redirect(url_for('.diffPushGen', kind = kind))

        else:
            ## assuming the curr_relation has a label atleast else no way are we going to isert it! ##TODO a check!!! Can be done at api time too!

            ## create
            ## crawl_obj is the copied object
            curr_id = gg.insertCoreGraphObjectHelper(kind, crawl_obj)

            ##MAJOR MAJOR TODO: if we are creating a hyperedgenode, we can directly also push all its relations! assuming all things are validated.
            ##if we are creating a node, all its relations that are connected to resolved nodes can all be pushed as such, saves a lot of time.
            ##again assuming that we have validated graph objects. 

            flash('Graph object created with id: '+ str(curr_id))
            flash(kind+ ' : '+CRAWL_ID_NAME +' : '+str(session[CRAWL_ID_NAME]))

            ##pop session objects
            session.pop(CRAWL_ID_NAME, None)
            session.pop(CURR_ID, None) ##redundant code!

            ##updateResolved PART
            gg.setResolvedWithID(kind, crawl_obj_original, curr_id)
            #change to original            
            return redirect(url_for('.show'))


##two params: number and uuid ?? in session!
@verifier.route('/diffPushGen/<string:kind>/', methods=["GET","POST"])
def diffPushGen(kind='node'):

    gg = GraphHandle()
    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    
    if session.get(CURR_ID) is None:
        return render_template("temp.html", homeclass="active", temptext='No diff tasks go to start task/match task first!')

    
    curr_id = session.get(CURR_ID)
    crawl_id = session.get(CRAWL_ID_NAME)

    
    crawl_obj_original = gg.getCrawlObjectByID(kind, CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)
    crawl_obj = gg.copyCrawlObject(kind, crawl_obj_original)
    

    naya = crawl_obj
    orig = gg.getOriginalCoreObject(kind, curr_id)
    orig.pull()

    
    new_labels, conf_props, new_props = gg.getNewLabelsAndPropsDiff(kind, orig, naya)
    

    if not request.form:

        return render_template("verifier_diff_gen.html", homeclass="active",
            new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya, crawl_id = session[CRAWL_ID_NAME], kind=kind)
    else:

        from app.constants import MVPLIST
        from app.utils.commonutils import Utils
        utils = Utils()

        
        for prop in conf_props:

            tosave = str(request.form[prop])

            
            ##the following code just checks if the props in conflict are list
            ##then we choose one of them, convert them to list and push
            ##but this seems to be a bad idea
            ##so commenting out

            






            flash(prop+' : '+str(tosave))
            ##update this prop in orig graph object!
            #orig[prop] = request.form[prop]
            orig[prop] = tosave ##naya prop/orig prop 

        
        for label in request.form.getlist('newlabels'):
            flash('Label: '+str(label))
            ##add this label to orig!
            orig.labels.add(label)

        
        for prop in new_props:
            
            value_list = request.form.getlist(prop)
            
            if len(value_list)==1: ##as only one value is going to be any way!

                tosave = str(request.form[prop])
                
               


                flash(prop+' : '+str(value_list[0]))
                ##add this prop to orig graph object!
                #orig[prop] = request.form[prop]
                orig[prop] = tosave ##naya prop/orig prop 



        ##name with alias patch
        aliascopy = utils.copyListOfStrings(orig['aliases']) 
        for alias in request.form.getlist('addtoalias'):
            flash('addtoalias: '+str(alias))
            alias = utils.processString(alias)
            if alias not in aliascopy:
                aliascopy.append(alias)
        orig['aliases'] = aliascopy
        
        

        orig.push()#one graph object resolved! 

        
        flash(kind+ ' : '+CRAWL_ID_NAME+' : '+ str(session[CRAWL_ID_NAME]))

        


        if kind=='node':
            #will be called when node's props are changed to update the row
            gg.updateIndexDBHelper(curr_id)

        gg.setResolvedWithID(kind, crawl_obj_original, curr_id)

        ##pop session objects
        session.pop(CRAWL_ID_NAME, None)
        session.pop(CURR_ID, None)
        
        return redirect(url_for('.show'))

        ##TODO: same validation checks like _ for wiki thing too 


