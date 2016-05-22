from app.verifier import verifier
from app.forms import form_error_helper, MergeNodeForm
from flask import render_template, flash, redirect, session, g, request, url_for, abort,current_app
import pandas as pd


@verifier.route('/')
def show():
    ##have a verifier page!
    ##show the begin task button!
    return render_template("verifier_home.html", homeclass="active")

@verifier.route('/diff/', methods=["GET","POST"])
def diff():
    
    import app.graphdb as t
    ##keep info about not shoiwng labels and not showing props 
    orig = t.orig() ##from the graph
    naya = t.node3() ##from the row

    orig.pull()
    print orig
    print '-------'

    new_labels = t.labelsToBeAdded(orig,naya) 
    conf_props,new_props = t.propsDiff(orig,naya)

    if not request.form:

        return render_template("verifier_diff.html", homeclass="active",
            new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya)
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
                
        print orig
        ##now can push!
        orig.push()


        return render_template("temp.html", homeclass="active",temptext="DIFF DONE!")




## TODO: this can be better!
@verifier.route('/match/', methods=["GET","POST"])
def match():
    if not request.form:
        from app.resolver import *      
        print resolveNode('xx') ##TODO: remove this!
        ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
        import app.graphdb as t
        row = t.node1()

        graphnodes = [t.orig(),t.node2(),t.node3()]
        return render_template("verifier_match.html", homeclass="active",
            row=row, graphnodes=graphnodes)
    else:
        ##get the matched_uuid! save it in sessnio or where-ever you want
        print request.form['match_uuid']
        return render_template("temp.html", homeclass="active",temptext="MATCH DONE!")



@verifier.route('/temp/',methods=["GET","POST"])
def temp():
    #TODO: check if temp.html works fine always
    temptext = "WTForms!!"''
    
    labels_list =  ['aaaa','bbbb','vvvv']
    new_props_list =  ['aaaa:hdjhjd','bbbb:jdhjkds','vvvv:dgjhdgd']
    form = MergeNodeForm()
    form.setLabels(labels_list)
    form.setNewProps(new_props_list)

    props = ['a','b','c']
    old = ['aa','bb','cc']
    naya = ['xx','yy','zz']
    form.setConfProps(props,old,naya)


    if form.validate_on_submit():
        try:
            print 'yayyyyyyayayayyayayayayayyayayayyayaya'
            flash (form.labels.data)
            flash (form.new_props.data)
            flash (form.conf_props.data)
            flash('Verifier Temp Success!')
            #print session
            #return redirect('home')
        except:
            flash('Temp Form Fail')
    else:
        form_error_helper(form)
    return render_template("veri_temp.html", homeclass="active",temptext=temptext, form = form)


@verifier.route('/temp2/',methods=["GET","POST"])
def temp2():
    props = ['a','b','c']
    old = ['aa','bb','cc']
    naya = ['xx','yy','zz']
    return render_template("veri_temp2.html", homeclass="active")

@verifier.route('/temp3/')
def temp3():
    meta, nodes, rels = mapSqlToGraph(current_app.config['MAPPINGS']+'/crawlerMap')
    print nodes
    print rels

    #do some dbwork here!
    ##why is this thing needed? to generate uuids for our app!
    from app.dbwork import *
    print createUuid(name='RandomRandom10000001')
    
    return render_template("temp.html", homeclass="active",temptext=nodes['1']['name'])

#called when the task begins
##can use the meta info in the dict returned to give the task a unique name
def mapSqlToGraph(filename):
    from app.graphdb import *
    from app.dbwork import *

    meta,ens,rels = crawlerMappings(filename)
    df = sqlQuerytoDF("select * from "+ meta['tablename']+" where resolved = 0 order by id limit 1;",
        current_app.config['CRAWL_DBHOST'], current_app.config['CRAWL_DBNAME'],
        current_app.config['CRAWL_DBUSER'], current_app.config['CRAWL_DBPASSWORD'])

    if len(df) == 0:
        return None, None

    mapNodes = {}
    mapRels = {}
    resolveNodesOn = {}
    resolveRelsOn = {}

    for en in ens:
        node, resolveOn = createNodeFromMapping(en,df)
        mapNodes[en['number']] = str(node) ##TODO: everything is a string for now! find a nice way out of this! May be a class!
        ##will have to deserialize at any cost!
        resolveNodesOn[en['number']] = resolveOn

    for rel in rels:
        startNode = mapNodes[rel['from']]
        endNode = mapNodes[rel['to']]
        link, resolveOn = createRelFromMapping(rel,startNode,endNode,df)
        mapRels[rel['number']] = str(link) ##TODO: everything is a string for now! Find a nice way out of this!
        resolveRelsOn[rel['number']] = resolveOn

    
    meta['row_id'] = df['id'][0] 
    return meta, mapNodes, mapRels, resolveNodesOn, resolveRelsOn


##TODO: move this code?? maybe, no!
def checkTaskExists():

    ##redundant code from mapSqlToGraph remove: TODO!
    from app.dbwork import *

    ##need to modularize and move this code from here! : TODO!
    meta,ens,rels = crawlerMappings(current_app.config['MAPPINGS']+'/crawlerMap')
    df = sqlQuerytoDF("select * from "+ meta['tablename']+" where resolved = 0 order by id limit 1;",
        current_app.config['CRAWL_DBHOST'], current_app.config['CRAWL_DBNAME'],
        current_app.config['CRAWL_DBUSER'], current_app.config['CRAWL_DBPASSWORD'])

    return len(df) != 0

def updateRow(tablename, row_id, ):
    ##redundant code from mapSqlToGraph remove: TODO!
    from app.dbwork import *

    ##need to modularize and move this code from here! : TODO!
    meta,ens,rels = crawlerMappings(current_app.config['MAPPINGS']+'/crawlerMap')
    df = sqlQuerytoDF("UPDATE "+ meta['tablename']+" SET resolved=2 WHERE id="+row_id+";",
        current_app.config['CRAWL_DBHOST'], current_app.config['CRAWL_DBNAME'],
        current_app.config['CRAWL_DBUSER'], current_app.config['CRAWL_DBPASSWORD'])




def findNextNodeNumberToResolve():
    ##before calling we know for sure that mapNodes exist!
    mapNodes = session.get('mapNodes')
    nodeKeys = mapNodes.keys()
    for key in nodeKeys:
        if key not in session.get('resolvedNodes'):
            return key
    return 'all'


@verifier.route('/startTask/')
def startTask():


    ##TODO: remove when not needed!
    session.pop('mapNodes', None)
    session.pop('mapRels', None)
    session.pop('resolvedNodes', None)
    session.pop('resolvedRels', None)
    session.pop('resolveNodesOn', None)
    session.pop('resolveRelsOn', None)
    session.pop('taskID', None)
    session.pop('tablename',None)
    session.pop('row_id',None)

    ##nos. to shwo how many rows left -- notify?

    ##TODO: check if four vars exist in session directly redirect to runTask
    #temptext = ''
    ##or may be invalidate all 4 vars on this and restart! the task id! TODO!
    if session.get('mapNodes') is not None:
        print 'startTask: in the middle of the task: '+str(session.get('taskID'))  
        return redirect(url_for('.runTask'))

    if checkTaskExists(): ##if task exists in crawl db!
        ##TODO: Provide a proceed button here
        print 'startTask: ckecked task exists!!'

        ##TODO: what if no row is there? ##checked done!
        ##call this for the time only, call mapSqlToGraph for the first time only
        meta, mapNodes, mapRels, resolveNodesOn, resolveRelsOn = mapSqlToGraph(current_app.config['MAPPINGS']+'/crawlerMap')
        ##won/t be none - mapNodes
        if mapNodes is None: ##this is just a redundant check!
            ## 'No pending tasks at all or all resolved. Heading back to startTask'
            return render_template("temp.html", homeclass="active", 
        temptext='No pending tasks as of now')
        else:
            ##give a new task id also!
            session['mapNodes']  = mapNodes
            session['tablename'] = meta['tablename'] ##added to set resolved=1
            session['row_id'] = str(meta['row_id']) ##added to set resolved=1
            session['mapRels'] = mapRels
            taskID = meta['tablename'] + str(meta['row_id']) ##useful logging TODO
            session['resolveNodesOn'] = resolveNodesOn ##props on which to resolve, map between entity number to which props to resolve
            session['resolveRelsOn'] = resolveRelsOn
            session['resolvedNodes'] = {} ##should be a  set? TODO
            session['resolvedRels'] = {}
            session['taskID'] = taskID
            print '\n\nstartTask: Beginning task ID: '+taskID+'\n\n'

        print 'startTask: now redirecting'
        return redirect(url_for('.runTask'))        
    else:
        temptext = 'No pending tasks'
    
    return render_template("temp.html", homeclass="active", 
        temptext=temptext)


@verifier.route('/runTask/')
def runTask():
    
    if session.get('mapNodes') is None:
        return render_template("temp.html", homeclass="active", temptext='No running tasks! Go to start task and check')       

    ##after the outer if mapNodes are not None in session, for sure!
    ##they are in session for sure!
    ##fetch the number in nodes to resolve, if all resolved just pop all and go to start_task
    ## session.pop('username', None)
    number = findNextNodeNumberToResolve()
    print '\n\n\n runtask: the number :'+str(number)+'\n\n\n'

    if number=='all': ##all have been resolved!
        ## pop all, redirect to start_task or resolve rels!
        ## TODO: rels left, remove them only when done with rels !!


        ##here is where when all rels have been resolved, all nodes have been resolved that we will set resolved to 1 for the row! rowid and tablename needed!
        from app.dbwork import updateResolved


        print 'runTask: CALLLLLLLLLLING UPDATE resolved!!!!'
        print session['tablename']
        print session['row_id']

        updateResolved(session['tablename'], session['row_id'], current_app.config['CRAWL_DBHOST'], current_app.config['CRAWL_DBNAME'],
        current_app.config['CRAWL_DBUSER'], current_app.config['CRAWL_DBPASSWORD'], resolved=1)

        session.pop('mapNodes', None)
        session.pop('mapRels', None)
        session.pop('resolvedNodes', None)
        session.pop('resolvedRels', None)
        session.pop('resolveNodesOn', None)
        session.pop('resolveRelsOn', None)
        session.pop('taskID', None)
        session.pop('curr_number',None)
        session.pop('curr_uuid',None)
        ##remove the two variables!
        session.pop('tablename', None)
        session.pop('row_id', None)

        ## 'No pending tasks at all or all resolved. Heading back to startTask'
        return redirect(url_for('.startTask'))
    else:
        ##if a number is returned to resolve call the next two methods! yayy!
        ##for nodes only! TODO: for relations accordingly!
        session['curr_number'] = number
        return redirect(url_for('.matchNodeNew'))
    
    
    #return render_template("temp.html", homeclass="active", 
     #   temptext='Running and resolving flow!')


##TODO: shoudlnt the number be in form or something??
@verifier.route('/matchNodeNew/',methods=["GET","POST"])
def matchNodeNew():

    if session.get('curr_number') is None:
         return render_template("temp.html", homeclass="active", temptext='No matching tasks go to start task/run task first!')


    import app.graphdb as t

    ##can get this info: number: from session as in diff!

    curr_number = session.get('curr_number')

    mapNodes = session.get('mapNodes')
    curr_node = t.deserializeNode(mapNodes[curr_number])


    if not request.form:
         ##py2neo object node

        matchingUUIDS = [250,251,252,253,350,351,352,353]


        ##use apache solr code here
        ##from app.resolver import *      
        ##print resolveNode('xx') ##TODO: remove this!
        ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
        
        
        graphnodes = t.getListOfNodes(matchingUUIDS)

        return render_template("verifier_match_node.html", homeclass="active",
            row=curr_node, graphnodes=graphnodes, taskID = session['taskID'], curr_number = curr_number)
    else:
        ##get the matched_uuid! save it in sessnio or where-ever you want
        #print request.form['match_uuid']

        flash(request.form['match_uuid'])

        if request.form['match_uuid']!='##NA##':            
            session['curr_uuid'] = request.form['match_uuid']
            return redirect(url_for('.diffPush'))
        else:
            ##creare a new uuid
            from app.graphdb import wrapCreateNode, getGraph
            
            ##assuming the curr_node has name property if not. no way are we going to insert it! ##TODO a check!!!
            ##create
            curr_node = wrapCreateNode(getGraph(),curr_node)

            ##set resolved node to correct number
            resolvedNodes = session.get('resolvedNodes')
            resolvedNodes[curr_number] = curr_node['uuid']
            session['resolvedNodes'] = resolvedNodes
            print '1. RESOLVED NODES!!!! :: ' + str(session['resolvedNodes'])

            ##pop current_number
            #pop curr_uuid
            session.pop('curr_number', None)
            session.pop('curr_uuid', None)


            flash('Node created with uuid: '+ str(curr_node['uuid']))

            flash('taskID '+str(session['taskID']))
            flash('resolvedNodes ',session['resolvedNodes'])
            

            #return render_template("temp.html", homeclass="active",temptext="NEW NODE CREATED DONE!")
            return redirect(url_for('.runTask'))
            ##TODO: second return


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

    if session.get('curr_uuid') is None:
         return render_template("temp.html", homeclass="active", temptext='No diff tasks go to start task/run task/match task first!')

    curr_number = session.get('curr_number')
    curr_uuid = session.get('curr_uuid')
    mapNodes = session.get('mapNodes')
    #session.pop('curr_uuid', None)
    #session.pop('curr_number', None)


    import app.graphdb as t
    ##keep info about not shoiwng labels and not showing props 
    orig = t.entity(curr_uuid)##from the graph
    naya = t.deserializeNode(mapNodes[curr_number]) ##from the row

    orig.pull()
    ##print 'orig: ' + str(orig)
    ##print '-------'
    ##print 'naya: ' + str(naya)
    ##print '-------'

    new_labels = t.labelsToBeAdded(orig,naya) 
    conf_props,new_props = t.propsDiff(orig,naya)

    if not request.form:

        return render_template("verifier_diff_node.html", homeclass="active",
            new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya, taskID = session['taskID'], curr_number = curr_number)
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

        resolvedNodes = session.get('resolvedNodes')
        resolvedNodes[curr_number] = curr_uuid
        session['resolvedNodes'] = resolvedNodes
        print '\n\ndiffpush. RESOLVED NODES!!!! :: ' + str(session['resolvedNodes'])+"\n\n"

        flash('taskID '+str(session['taskID']))
        flash('resolvedNodes ',session['resolvedNodes'])

        return redirect(url_for('.runTask'))


        #return render_template("temp.html", homeclass="active",temptext="DIFF DONE!")



    # #uuid = request.args.get('uuid') ##not working at all since immutable
    # #push something to this uuid here!

    # ##some mechanism will give us a new py2neo node ---> after the selection of the diffs, based on labels, props, etc.
    # ##we will write a method to push that new py2neo node if uuid exists!

    # ##TODO: show a start task button here
    # return render_template("temp.html", homeclass="active", 
    #     temptext='Push something new to '+ str(uuid)+' task completed') ##str beacuse of None