from app.verifier import verifier
from app.forms import form_error_helper, MergeNodeForm
from flask import render_template, flash, redirect, session, g, request, url_for, abort,current_app
import pandas as pd


@verifier.route('/')
def show():
    return render_template("temp.html", homeclass="active", temptext='verifier')

@verifier.route('/diff/')
def diff():
    import app.graphdb as t

    ##keep info about not shoiwng labels and not showing props 
    orig = t.orig() ##from the graph
    naya = t.node3() ##from the row
    
    new_labels = t.labelsToBeAdded(orig,naya)    
    conf_props,new_props = t.propsDiff(orig,naya)


    return render_template("verifier_diff.html", homeclass="active",
        new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya)

## TODO: this can be better!
@verifier.route('/match/')
def match():
    from app.resolver import *
    print resolveNode('xx')
    ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
    import app.graphdb as t
    row = t.node1()

    graphnodes = [t.orig(),t.node2(),t.node3()]
    return render_template("verifier_match.html", homeclass="active",
        row=row, graphnodes=graphnodes)

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
    nodes, rels = mapSqlToGraph(current_app.config['MAPPINGS']+'/crawlerMap')
    print nodes
    print rels

    #do some dbwork here!
    ##why is this thing needed? to generate uuids for our app!
    from app.dbwork import *
    print createUuid(name='RandomRandom10000001')
    
    return render_template("temp.html", homeclass="active",temptext=nodes['1']['name'])


def crawlerMappings(crawlFile):
    
    crawlFile = open(crawlFile)

    ## format of file:
    ## metainfo key value pairs
    ## ens
    ## rels etc. in order

    ens = []
    rels = []
    metainfo = {}
    currdict = {}
    curr_ch = '-'

    for line in crawlFile.readlines():
        line = line.strip()
        if line[0]=='#':

            ##adjusting the old one
            if curr_ch=='e':
                ens.append(currdict)
            elif curr_ch == 'r':
                rels.append(currdict)

            ##adjusting for the new one
            if line[1]=='e':
                ##an entity is what we are reading
                currdict = {}
                curr_ch='e'
            else:
                currdict = {}
                curr_ch='r'
                ##a relation is what we are reading
        elif curr_ch!='-':
            prop = line[0:line.find(':')].strip()
            value = line[line.find(':')+1:].strip()
            if(prop!='number' and prop!='from' and prop!='to'):
                #split
                value = value.split(',')
                #strip
                value = map(str.strip, value)
            currdict[prop] = value
        else:
            prop = line[0:line.find(':')].strip()
            value = line[line.find(':')+1:].strip()
            metainfo[prop] = value
    if curr_ch=='e':
        ens.append(currdict)
    elif curr_ch=='r':
        rels.append(currdict)
    
    return metainfo,ens,rels
    

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

    for en in ens:
        node = createNodeFromMapping(en,df)
        mapNodes[en['number']] = str(node) ##TODO: everything is a string for now! find a nice way out of this! May be a class!

    for rel in rels:
        startNode = mapNodes[rel['from']]
        endNode = mapNodes[rel['to']]
        link = createRelFromMapping(rel,startNode,endNode,df)
        mapRels[rel['number']] = str(link) ##TODO: everything is a string for now! Find a nice way out of this! 
    
    return mapNodes, mapRels

def checkTaskExists():
    return True

@verifier.route('/startTask/')
def startTask():   
    ##TODO: check if four vars exist in session directly redirect to runTask
    #temptext = ''
    ##or may be invalidate all 4 vars on this and restart! the task! TODO!
    if session.get('mapNodes') is not None:
        return redirect(url_for('.runTask'))

    if checkTaskExists():
        ##TODO: Provide a proceed button here
        print 'ckeck task exists!!'
        temptext = 'Task exists click to proceed'
        ##redirecting for now
        print 'reeeeeeeeeeeeeediiiiiiirectiiiiing'
        return redirect(url_for('.runTask'))        
    else:
        temptext = 'No pending tasks'
    
    return render_template("temp.html", homeclass="active", 
        temptext=temptext)

@verifier.route('/runTask/')
def runTask():
    
    if session.get('mapNodes') is None:
        ##TODO: what if no row is there? ##checked done!
        mapNodes, mapRels = mapSqlToGraph(current_app.config['MAPPINGS']+'/crawlerMap')
        if mapNodes is None:
            ## 'No pending tasks at all or all resolved. Heading back to startTask'
            return redirect(url_for('.startTask'))
        else:
            session['mapNodes']  = mapNodes
            session['mapRels'] = mapRels
            resolveNodes = {}
            resolveRels = {}
            session['resolveNodes'] = resolveNodes
            session['resolveRels'] = resolveRels

    ##after the outer if mapNodes are not None in session, for sure!
    ##they are in session for sure!
    ##fetch the number in nodes to resolve, if all resolved just pop all and go to start_task
    ## session.pop('username', None)
    number = findNextNodeNumberToResolve() 
    if number=='all':
        ## pop all, redirect to start_task or resolve rels!
        ## TODO: rels left
        session.pop('mapNodes', None)
        session.pop('mapRels', None)
        session.pop('resolveNodes', None)
        session.pop('resolveRels', None)
        ## 'No pending tasks at all or all resolved. Heading back to startTask'
        return redirect(url_for('.startTask'))
    else:
        ##if a number is returned to resolve call the next two methods! yayy!
        return redirect(url_for('.matchNew',number = number))
    
    
    return render_template("temp.html", homeclass="active", 
        temptext='Running and resolving flow!')

def findNextNodeNumberToResolve():
    ##before calling we know for sure that mapNodes exist!
    mapNodes = session.get('mapNodes')
    nodeKeys = mapNodes.keys()
    for key in nodeKeys:
        if key not in session.get('resolveNodes'):
            return key
    return 'all'

##TODO: shoudlnt the number be in form or something??
@verifier.route('/matchNew/<string:number>/')
def matchNew(number):
    ## TODO!!
    ## form showing all matched uuids
    ## fetch one uuid from the form
    ## let uuid = 25 for '1' and 28 for '2' for sake of simplicity here
    ## forward to diffPush method with number and uuid

    ##handle the case when no uuid is resturned TODO!
    ##just create a new node in above case
    session['curr_number'] = number
    if number=='1':
        session['curr_uuid'] = 25
    else:
        session['curr_uuid'] = 28

    ##g is creating a lot of problems but why!!
    ##have to use session for such a thing! bad! TODO! check what is the solution!

    return redirect(url_for('.diffPush'))
    return render_template("temp.html", hosmeclass="active", 
        temptext='Matching '+number)


##two params: number and uuid ?? in session!
@verifier.route('/diffPush/')
def diffPush():
    number = session.get('curr_number')
    uuid = session.get('curr_uuid')
    session.pop('curr_uuid', None)
    session.pop('curr_number', None)

    #uuid = request.args.get('uuid') ##not working at all since immutable
    #push something to this uuid here!

    ##some mechanism will give us a new py2neo node ---> after the selection of the diffs, based on labels, props, etc.
    ##we will write a method to push that new py2neo node if uuid exists!

    ##TODO: show a start task button here
    return render_template("temp.html", homeclass="active", 
        temptext='Push something new to '+ str(uuid)+' task completed') ##str beacuse of None

