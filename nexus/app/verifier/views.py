from app.verifier import verifier
from flask import render_template, flash, redirect, session, request, url_for, g
from app.models.graphmodels.graph_handle import GraphHandle

@verifier.route('/')
def show():
    # have a verifier page!
    # show the begin task button!
    gg = GraphHandle()

    # CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    # ##This is needed whenever a new task is started
    # ##Task would mean anything node resolution, rel resolution, or hyperedge resolution
    # session.pop(CRAWL_ID_NAME, None)
    # session.pop(CURR_ID, None)

    unresolvedTotal, unlockedUnresolvedTotal, immediateUnResolvedTotal = gg.getCrawlNodeStats()

    r_unresolvedTotal, r_beingResolved, r_immediateUnResolvedTotal = gg.getCrawlRelationStats()

    n_wiki_total, n_wiki_actual = gg.getWikiNodeStats()

    r_wiki_total, r_wiki_actual = gg.getWikiRelationStats()

    h_unresolvedTotal, h_immediateUnResolvedTotal = gg.getCrawlHyperEdgeNodeStats()

    return render_template("verifier_home.html", homeclass="active",
        unlockedUnresolvedTotal = unlockedUnresolvedTotal,unresolvedTotal = unresolvedTotal, immediateUnResolvedTotal = immediateUnResolvedTotal,
        r_unresolvedTotal = r_unresolvedTotal, r_immediateUnResolvedTotal = r_immediateUnResolvedTotal,
        r_beingResolved = r_beingResolved, h_unresolvedTotal = h_unresolvedTotal, h_immediateUnResolvedTotal = h_immediateUnResolvedTotal,
        n_wiki_total=n_wiki_total, n_wiki_actual = n_wiki_actual, r_wiki_total = r_wiki_total, r_wiki_actual = r_wiki_actual)

def getTaskType():
    from app.constants import SESSION_TASKTYPE_NAME, SESSION_CRAWL_VAL, SESSION_WIKI_VAL
    tasktype = request.args.get(SESSION_TASKTYPE_NAME)
    if tasktype is None:
        print 'should not be here at aaaaaaaaaaaaaaaannnnnnnnnnny cost!!!'
        tasktype = SESSION_CRAWL_VAL
    ##why we did not use a new parameter
    ##will not have to change match in all places
    print "[getTaskType: tasktype: %s]" %(tasktype)
    return tasktype

def taskTypeValidateHelper():

    from app.constants import SESSION_TASKTYPE_NAME
    tasktype = getTaskType()
    print "[taskTypeValidateHelper: SESSION_TASKTYPE_NAME in session: %s]" %(session.get(SESSION_TASKTYPE_NAME))
    ##why we choose request.args and not functional parameters
    return session.get(SESSION_TASKTYPE_NAME) == tasktype

@verifier.route('/beginagain/<string:choice>/<string:kind>/')
def beginagain(choice, kind):


    ##kind should be from session
    ##session.get('kind') will be one thing either node or rel right
    ##similarly for tasktype
    ##TODO: check

    gg = GraphHandle()

    CRAWL_ID_NAME, CURR_ID = gg.getTwoVars(kind)

    tasktype = getTaskType()

    if session.get(CRAWL_ID_NAME) is None:
        flash("You don't have any on-going tasks. Redirecting to start page.")
        return redirect(url_for('.show'))

    if choice == 'options':
        flash('Selected options')
        return render_template("verifier_begin_again.html", homeclass="active", kind=session.get('kind'))

    elif choice == 'resume':

        flash('Selected resume')

        if session.get(CRAWL_ID_NAME) is None:
            return redirect(url_for('.show'))

        if session.get(CURR_ID) is None:
            return redirect(url_for('.match', kind=session.get('kind'), tasktype = session.get('tasktype') ))

        return redirect(url_for('.diffPushGen', kind=session.get('kind'), tasktype = session.get('tasktype') ))

    elif choice == 'sessionclear':
        flash('Selected sessionclear')

        clearVerifierSessionAll()

        flash('Locks will be eventually released by bot. Your task is cleared.')

        return redirect(url_for('.show'))

    elif choice == 'releaseall':
        flash('Selected releaseall')

        clearVerifierSessionAll()
        releaseAllMyLocksNow()

        return redirect(url_for('.show'))

    else:
        flash('Not a valid option in beginagain!')
        return render_template("temp.html", homeclass="active", temptext='Not a valid option')

def releaseAllMyLocksNow():
    gg = GraphHandle()
    nc, rc = gg.crawldb.releaseLocks(userid=session['userid'])
    flashstr = "User explicitly asked to release (%s,%s) locks with userid %s" %(str(nc),str(rc),session['userid'])
    flash(flashstr)
    flash('Your locks released. Your task cleared.')

@verifier.route('/startTask/<string:tasktype>/<string:kind>/')
def startTask(kind, tasktype): ##no point of defaulting to 'node', doesn't take it


    ##XXX-DONE:there has to be a differentitaor for moderator tasks
    #either in session or somewhere else like in this fn as a request argument

    gg = GraphHandle()

    allVars = gg.getAllVars()
    flag = False
    retKind = None

    #XXX-DONE: for wiki tasks too, let it go to beginagain page
    #XXX: do patch and correct
    for (var,retkind) in allVars:
        if session.get(var) is not None:
            flash('You already have ongoing tasks in your session. Redirecting to beginagain.')
            return redirect(url_for('.beginagain', kind = retkind, choice = "options", tasktype = tasktype))

    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    # ##This is needed whenever a new task is started
    clearVerifierSessionAll()

    #also you can do one task at a time: verify or mod.
    # for (var,retkind) in allVars:
    #     ## imp
    #     ## so baiscally when a new task is started old task gets stale.
    #     ## so if you are on old task page, that could create a problem
    #     ## that is why the checks are for crawl_id, kind, and curr_id in match/diff
    #     session.pop(var, None)
    # session.pop('kind', None)

    # ##Obsolete now TODO: remove
    # ##TODO: check if session vars exist in session directly redirect to runTask
    # if session.get(CRAWL_ID_NAME) is not None:
    #     print 'startTask: in the middle of a resolution task of kind '+kind+' for graph object : '+str(session.get(CRAWL_ID_NAME))
    #     return redirect(url_for('.match', kind = kind))

    ##XXX: pass one more variable which type of task: wiki or crawl

    ##TWO WORK: areTasksLeft and view for mod, then we can test both
    ##part 1 should be completed
    ##also check if kind variable needed in beginagain
    if gg.areTasksLeft(kind, tasktype): ##if task exists in crawl db!

        from app.constants import SESSION_TASKTYPE_NAME

        print '[startTask: ckecked tasks to resolve exist for kind'+kind+'!! and tasktype:'+tasktype+' ]'

        graphobj = gg.nextTaskToResolve(kind, tasktype, session.get('userid')) ##XXX: similarly call: our wiki method

        print '[startTask: graphobj: %s]' %(str(graphobj))

        session[CRAWL_ID_NAME] = graphobj[CRAWL_ID_NAME]
        session['kind'] = kind ##adding kind to session as well.
        session[SESSION_TASKTYPE_NAME] = tasktype ##patch for wiki/crawl ##removed later

        print '[\n\nstartTask: Beginning resolution for graph obj with crawl id: '+graphobj[CRAWL_ID_NAME]+'\n\n]'
        print '[startTask: tasktype %s]' %(tasktype)
        print '[startTask: now redirecting]'

        if tasktype=='wiki':
            from app.constants import RESOLVEDWITHUUID, RESOLVEDWITHRELID
            crawl_obj_original = gg.getCrawlObjectByID(kind, CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)
            if kind == 'node':
                session[CURR_ID] = crawl_obj_original[RESOLVEDWITHUUID]
            else:
                session[CURR_ID] = crawl_obj_original[RESOLVEDWITHRELID]
            return redirect(url_for('.diffPushGen', kind = kind, tasktype = tasktype))

        ##else if defaults to :
        return redirect(url_for('.match', kind = kind, tasktype = tasktype))

    ##if the above if doesnt work, comes here
    ##TODO: .show redirect
    temptext = 'No pending graph objects of kind %s and tasktype %s to resolve, please go back'
    temptext = temptext % (kind, tasktype)
    return render_template("temp.html", temptext=temptext)


@verifier.route('/match/<string:kind>/', methods=["GET", "POST"])
def match(kind):

    gg = GraphHandle()
    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)

    if session.get(CRAWL_ID_NAME) is None:
        return redirect(url_for('.show'))

    if session.get('kind') is None or session.get('kind') !=kind:
        flash('Kinds do not match, you must have began working in some other tab.')
        ###XXX: tasktype?
        return redirect(url_for('.beginagain',kind=session.get('kind'), choice='options'))

    #----- PATCH for tasktype -----#

    ##XXX: if tasktype wiki and curr_id exist
    ## do we really need to use this request.args??
    ## can just if session me tasktype not none and tasktype is wiki??
    ## or setting both - one way or another! or change all :(

    tasktype = getTaskType()

    if not taskTypeValidateHelper():
        flash('Tasktypes do not match, you must have began working in some other tab.')
        ##redirecting to begin again, so that the user can
        ##go to his/her original task
        ###XXX: tasktype?
        return redirect(url_for('.beginagain',kind=session.get('kind'), choice='options'))

    from app.constants import SESSION_WIKI_VAL
    if tasktype == SESSION_WIKI_VAL:
        if session.get(CURR_ID) is None:
            # that means wiki is set but CURR_ID is not set,
            # (or CRAWL_ID_NAME is not set -- already check above)
            # this should not be the case
            # clear all session
            # release all locks and got to .show
            # XXX: should work fine do check
            return redirect(url_for('.beginagain',kind=session.get('kind'), choice='releaseall'))
        else:
            ##will have to go to diff
            ##XXX:check this!
            ##XXX: tasktype?
            return redirect( url_for('.diffPushGen',kind=session.get('kind'), tasktype=tasktype))

    # --- tasktype patch end ----- #


    crawl_obj_original = gg.getCrawlObjectByID(kind, CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)


    lockprop, msg = gg.checkLockProperties(crawl_obj_original, session.get('userid'))
    if lockprop != 'allowed':

        ##IMP : Even if your lock is removed by bot, and if you do anything to call match or diff both, you will be redirected to .show route, and your session vars will be automatically removed

        msg  =  msg +" for kind " +str(kind)
        ##also will have to remove session variables
        clearVerifierSessionAll()
        # session.pop(CRAWL_ID_NAME, None)
        # session.pop(CURR_ID, None )
        # session.pop('kind', None)
        flash(msg)
        return redirect(url_for('.show'))


    ##essential node meta is required when actually creating the node
    ##also will be required when resolving the relation, though can be taken from original

    crawl_obj = gg.copyCrawlObject(kind, crawl_obj_original)


    ##TODO: validation as well! What actually? I forgot!

    if not request.form:

        algo = request.args.get('postalgo')

        graphobjs = gg.matchPossibleObjects(kind, crawl_obj, crawl_obj_original)
        connected_ens = gg.getDirectlyConnectedEntitiesCrawl(kind, crawl_obj_original) ##will be none if not hyperedgenode for now
        flash('Selected post-algo: '+str(algo))

        return render_template("verifier_match.html", homeclass="active",
            row=crawl_obj, graphobjs=graphobjs, ID=session[CRAWL_ID_NAME], kind=kind,
            idname=gg.getCoreIDName(kind), connected_ens=connected_ens, crawl_obj_original=crawl_obj_original)

    else:

        if session[CRAWL_ID_NAME] != request.form['##crawl_id##']:
            flash("The crawl_id does not match with the session's")
            return redirect(url_for('.beginagain',choice='options', kind=kind))

        if request.form.get('match_id') is None:
            flash('Please select a matching option to proceed')
            return redirect(url_for('.match', kind = kind, tasktype = tasktype))


        if request.form['match_id']=='##ID##':
            idval = request.form['input_id']

            ##TODO: validation if such id for this kind exists
            if idval is None or idval.strip() == '':
                flash('nothing given in id text box')
                return redirect(url_for('.match', kind = kind, tasktype = tasktype))
            session[CURR_ID] = request.form['input_id']
            return redirect(url_for('.diffPushGen', kind = kind, tasktype='crawl'))

        if request.form['match_id']!='##NA##':
            session[CURR_ID] = request.form['match_id']
            print session[CRAWL_ID_NAME] + ' inside sessionnnnnnnnnn'
            return redirect(url_for('.diffPushGen', kind = kind, tasktype='crawl'))

        if request.form['match_id']=='##NA##':
            ## assuming the curr_relation has a label atleast else no way are we going to insert it!
            ##TODO a check for above one type for relation!!! Can be done at api time too!

            ## create
            ## crawl_obj is the copied object
            curr_id = gg.insertCoreGraphObjectHelper(kind, crawl_obj)

            ##MAJOR MAJOR TODO: if we are creating a hyperedgenode, we can directly also push all its relations! assuming all things are validated.
            ##if we are creating a node, all its relations that are connected to resolved nodes can all be pushed as such, saves a lot of time.
            ##again assuming that we have validated graph objects.

            flash('Graph object created with id: '+ str(curr_id))
            flash(kind+ ' : '+CRAWL_ID_NAME +' : '+str(session[CRAWL_ID_NAME]))

            ##step: get the recenlty inserted object
            curr_obj = gg.getOriginalCoreObject(kind, curr_id)

            changeid, numrows = gg.resolveAndProvenance(kind, curr_id, curr_obj, None, crawl_obj_original, session['userid'])

            # ##Provenance patch
            # ##DONE: set resolved and also other props here, verified by, verified at, etc.
            # gg.setResolvedWithID(kind, crawl_obj_original, curr_id, session['userid'])
            # #change to original
            #
            # numrows = gg.provenanceCore(None, curr_obj, curr_id, crawl_obj_original, kind)

            # ##pop session objects
            # ##only after all the resolution complete and done
            # gg.crawldb.unlockObject(crawl_obj_original)
            clearVerifierSessionAll()

            # ##Infact resolution for ID should be done here
            # ##TODO: gg.crawldb.unlockObject(crawl_obj_original) should be done here alongside clearVerifierSessionAll

            flashmsg =  "[match: changeid: %s || numrows: %s || kind: %s || id: %s]" %(changeid, numrows, kind, curr_id)
            print flashmsg
            flash(flashmsg)

            return redirect(url_for('.show'))

        else:
            flash("Match_id not recognized. Start over again.")
            return redirect(url_for('.show'))


##two params: number and uuid ?? in session!
@verifier.route('/diffPushGen/<string:kind>/', methods=["GET","POST"])
def diffPushGen(kind):

    gg = GraphHandle()
    CRAWL_ID_NAME, CURR_ID  = gg.getTwoVars(kind)


    if session.get(CURR_ID) is None:
        msg = 'No diff tasks go to start task/match task first!'
        flash(msg)
        return redirect(url_for('.show'))

    if session.get('kind') is None or session.get('kind') !=kind:
        flash('Kinds do not match, you must have began working in some other tab.')
        redirect('.beginagain',kind=session.get('kind'),choice='options')

    tasktype = getTaskType()

    ## TASKTYPE PATCH -------
    if not taskTypeValidateHelper():
        print 'why o why here!!!'
        print kind
        flash('Tasktypes do not match, you must have began working in some other tab.')
        ##redirecting to begin again, so that the user can
        ##go to his/her original task
        ###XXX: tasktype?
        print session.get('kind')
        return redirect(url_for('.beginagain',kind=session.get('kind'), choice='options'))
    ## TASKTYPE PATCH -------


    curr_id = session.get(CURR_ID)
    crawl_id = session.get(CRAWL_ID_NAME)

    crawl_obj_original = gg.getCrawlObjectByID(kind, CRAWL_ID_NAME, session[CRAWL_ID_NAME], isIDString = True)

    ##here we check if actually the node is locked
    ##only then proceed

    ##TODO: check if same user locked, and lock by same user
    ##TODO: relations too, keep as general as possible
    ##remove locks from general nodes too
    ##let the code be fixed then we can copy code to match too
    ##change the count in the view too

    lockprop, msg = gg.checkLockProperties(crawl_obj_original, session.get('userid'))
    if lockprop != 'allowed':
        msg  =  msg +" for kind " +str(kind) ##Adding the same code as match
        ##also will have to remove session variables
        clearVerifierSessionAll()
        # session.pop(CRAWL_ID_NAME, None)
        # session.pop(CURR_ID, None )
        # session.pop('kind', None)
        flash(msg)
        return redirect(url_for('.show'))


    crawl_obj = gg.copyCrawlObject(kind, crawl_obj_original)

    naya = crawl_obj
    orig = gg.getOriginalCoreObject(kind, curr_id)
    orig.pull()


    new_labels, conf_props, new_props = gg.getNewLabelsAndPropsDiff(kind, orig, naya)
    print 'just before diffffffffffffff'
    print new_props, new_labels, new_props

    if not request.form:

        if new_labels == [] and new_props == [] and conf_props == []:
            ##
            flash('Objects match prop by prop, label by label, just setting resolved id in crawldb')
            # print 'Objects match prop by prop, label by label, just setting resolved id in crawldb'
            return resolveFast(gg, kind, crawl_obj_original, curr_id, CRAWL_ID_NAME, CURR_ID)

        print session.get(CRAWL_ID_NAME,'Bhai kuch nahi aaaya!')


        return render_template("verifier_diff_gen.html", homeclass="active",
            new_labels=new_labels, conf_props=conf_props, new_props=new_props, orig=orig, naya=naya, crawl_id = session[CRAWL_ID_NAME], kind=kind, tasktype=tasktype, crawl_obj_original=crawl_obj_original)
    else:

        from app.constants import MVPLIST
        from app.utils.commonutils import Utils
        utils = Utils()

        ##for provenance
        old_obj = gg.copyCrawlObject(kind,orig)

        ##first check if justresolve has been selected
        value_list = request.form.getlist('justresolve')

        if len(value_list)==1:

            ##redundant code, we know its the only option, would have been selected
            justresolve = request.form['justresolve']
            print justresolve

            flash('Nothing will be pushed. Resolving just like that')
            return resolveFast(gg,kind,crawl_obj_original, curr_id, CRAWL_ID_NAME, CURR_ID)
            # return redirect(url_for('.show'))

        if not checkDiffSelected(conf_props,new_props,new_labels):
            flash('You selected nothing. Please select something. <br/> Or you can select JUST RESOLVE.')
            return redirect(url_for('.diffPushGen',kind=kind, tasktype = tasktype))

        ##we are really going to update something, if reach here
        for prop in conf_props:

            tosave = str(request.form[prop])


            ##the following code just checks if the props in conflict are list
            ##then we choose one of them, convert them to list and push
            ##but this seems to be a bad idea
            ##so commenting out


            flash(prop+' : '+str(tosave))
            ##update this prop in orig graph object!
            #orig[prop] = request.form[prop]

            if str(tosave)!=str(orig[prop]): ##added patch before provenance,
                ##if creates problem, can remove
                orig[prop] = tosave ##naya prop/orig prop


        for label in request.form.getlist('newlabels'):
            flash('Label: '+str(label))
            ##add this label to orig!
            orig.labels.add(label)


        for prop in new_props:

            value_list = request.form.getlist(prop)
            if len(value_list)==1: ##as only one value is going to be any way
                tosave = str(request.form[prop])

                flash(prop+' : '+str(value_list[0]))
                ##add this prop to orig graph object!
                #orig[prop] = request.form[prop]
                orig[prop] = tosave ##naya prop/orig prop


        ##name with alias patch
        ##NOTE: we didnt processString when savinf first alias!
        ##That's why here too!
        ##TODO: move to graph_handle
        if kind == 'node':
            if orig['aliases'] is None:
                orig['aliases'] = [orig['name']] ##the new name at any cost
            aliasoriglist = utils.copyList(orig['aliases'])
            aliasmodifylist = utils.copyListOfStrings(orig['aliases'])
            flag = False
            for aliasorig in request.form.getlist('addtoalias'):
                aliasmodify = utils.processString(aliasorig)
                if aliasmodify not in aliasmodifylist:
                    flash('addtoalias: '+str(aliasorig))
                    flag = True
                    aliasoriglist.append(str(aliasorig))
            if flag:
                orig['aliases'] = aliasoriglist

        orig.push()#one graph object resolved!


        flash(kind+ ' : '+CRAWL_ID_NAME+' : '+ str(session[CRAWL_ID_NAME]))

        if kind=='node':
            #will be called when node's props are changed to update the row
            gg.updateIndexDBHelper(curr_id)

        curr_obj = orig

        # provenance patch
        changeid, numrows = gg.resolveAndProvenance(kind, curr_id, curr_obj, old_obj, crawl_obj_original, session['userid'])
        clearVerifierSessionAll()

        flashmsg =  "[diffPushGen: changeid: %s || numrows: %s || kind: %s || id: %s]" %(changeid, numrows, kind, curr_id)
        print flashmsg
        flash(flashmsg)

        return redirect(url_for('.show'))

        ##TODO: same validation checks like _ for wiki thing too


def resolveFast(gg, kind, crawl_obj_original, curr_id, CRAWL_ID_NAME, CURR_ID):
    # gg.setResolvedWithID(kind, crawl_obj_original, curr_id, session['userid'])
    # gg.crawldb.unlockObject(crawl_obj_original)

    ##resolved methods has unlock work too
    ##since this is a fast resolve, no need to update any metadata
    ##the work is only on the crawl object
    ##note here too the session is cleared after resolve

    gg.resolveAndProvenance(kind, curr_id, None, None, crawl_obj_original, session['userid'])
    #  no need of getting the changeid or numrows as both will be None in this case

    clearVerifierSessionAll()

    flash('Session cleared. Object unnlocked. Object resolved.')

    return redirect(url_for('.show'))

def checkDiffSelected(conf_props, new_props, new_labels):
    '''
        returns True if some option selected in diff page
        else returns False
    '''
    flag = False

    for prop in conf_props:
        flag = True ##always selected
        break
    if flag:
        return flag

    for prop in new_props:
            value_list = request.form.getlist(prop)
            if len(value_list)==1: ##as only one value is going to be any way
                flag = True
                break
    if flag:
        return flag

    for label in request.form.getlist('newlabels'):
        flag = True
        break

    return flag

def clearVerifierSessionAll():
    gg = GraphHandle()
    allVars = gg.getAllVars()
    for a,b in allVars:
        session.pop(a, None)
    session.pop('kind', None)
    session.pop('tasktype',None) ##added new
