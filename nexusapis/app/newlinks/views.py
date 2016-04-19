from app.newlinks import newlinks
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify
from utils_crawler import *
from app.apigraphdb import *

##Usage: http://localhost:5000/newlinks/randomrandom/?_token=NexusToken
## http://localhost:5000/newlinks/randomrandom?_token=NexusToken
@newlinks.route('/randomrandom/')
def show():
    return jsonify({'message':'randomrandom success'}), 200
    ##The below can b removed: not needed at all, checked completely
    # resp = Response(response=jsonify({'message':'randomrandom'}), 
    #     status=200, 
    #     mimetype="application/json")
    # return(resp)

@newlinks.route('/')
def home():
    return jsonify({'message':'Token works!'}), 200


##Usage: http://localhost:5000/newlinks/createtask/?_token=NexusToken2&taskname=wow77
@newlinks.route('/createtask/', methods=['POST'])
def createTask():

    ##for a token --> dict of tasks
    ##for a task --> dict of props

    tokenid = request.args.get('_token')

    token_task_dict= session.get(tokenid,{})

    taskname = request.args.get('taskname',None)

    ##if no task name is given in request arguments
    if taskname is None:
        return jsonify({'message': 'createtask: Cannot create, no taskname given to create'}), 400

    old_task = token_task_dict.get(taskname, None)
    print old_task

    ##if task name already exists against the current token
    if old_task is not None:
        return jsonify({'message': 'createtask: task already exists'}), 400


    timenow = getTimeNow()

    to_save_dict = {}
    to_save_dict['_token'] = tokenid
    to_save_dict['taskname'] = taskname
    to_save_dict['starttime'] = timenow
    to_save_dict['status'] = 'Active'

    token_task_dict[taskname] = to_save_dict

    session[tokenid] = token_task_dict

    return jsonify(token_task_dict), 201


##Usage: http://localhost:5000/newlinks/getalltasks/?_token=NexusToken2
@newlinks.route('/getalltasks/', methods=['GET'])
def getAllTasks():

    tokenid = request.args.get('_token')

    token_task_dict= session.get(tokenid,None)

    ##if no task name is given in request arguments
    ##TODO: decide if 200 or 400 bad request or success
    if token_task_dict is None:
        return jsonify({'message': 'getalltasks: No task at all'}), 200

    return jsonify(token_task_dict), 200


def error_helper(message,statuscode):
    return jsonify({'message':message}), statuscode

@newlinks.route('/pushlinked/', methods=['POST'])
def pushLinked():

    
    tokenid = request.args.get('_token')

    print 'datttttttta'
    print request.data
    print 'jsonnnnnnnn'
    print request.json

    if not request.json: ##is a dict!!
        return error_helper("Not JSON Data",400)

    required_master_props = ['taskname', 'description', 'fetchdate', 'sourceurls', 'entities']
    for prop in required_master_props:
        if not prop in request.json:
            return error_helper(str(prop)+" not in json data", 400)    
    
    taskname = request.json['taskname']

    ## MAJOR TODO!
    ## some props are interanally reserved crawl_en_id not allowed for nodes
    ## what about ternary relations?
    ## 
    ## check for strings 
    ## validation checks: if task exists, 
    ## ids repeated in nodes in json and in actual 
    ## ids repeated in relations
    ## source_urls known in particular format
    ## fetch date in format
    ## allowed labels
    ## props allowed
    ## values all in strings or particular format?
    ## apis to add a new property in allowed dict with its description?
    ## ids ints?
    ## check if nodeid already exists in temp graph db, or relid
    ## create indexes and contsraints will have to add an internal label and internal relation label

    ##MAJOR TODO what to do about metadata?
    ##"description": "Naveen Jindal Connections",
    ##"fetchdate": "01/01/2011",
    ##use this metadata


    entities = request.json['entities']
    relations = []
    if 'relations' in request.json:
        relations = request.json['relations']

    
    subgraph = {}
    subgraph['_token'] = tokenid
    subgraph['taskname'] = taskname
    subgraph['pushtime'] = getTimeNow()
    subgraph['sourceurls'] = request.json['sourceurls']
    subgraph['fetchdate'] = request.json['fetchdate']

    nodes = {}
    links = {}

    ##MAJOR TODO reserved keywords and required keywords list
    ##MAJOR TODO format and pattern against keywords with regex

    required_endict_props = ['labels','properties','id']
    reserved_en_props = ['crawl_en_id','resolvedWithUUID','taskname','token','_token','workname','date','time','resolvedDate','resolvedAgainst','verifiedBy','resolvedBy','verifiedDate','update','lastUpdatedBy','lastUpdatedOn']
    required_en_props = ['name'] ##inside entity['properties']

    for en in entities:

        for prop in required_endict_props:
            if not prop in en:
                return error_helper(str(prop)+' required attribute missing for an entity', 400) 

        #print entities[en]
        nodeid = en['id']
        if nodeid in nodes:
            return error_helper('id repeated under entities',400)
        
        if not len(en['labels'])>0:
            return error_helper('Labels list empty for an entity', 400)

        for prop in required_en_props:
            if not prop in en['properties']:
                return error_helper(str(prop)+' required property missing for an entity', 400)

        for prop in reserved_en_props:
            if prop in en['properties']:
                return error_helper(str(prop)+' reserved property not allowed explicitly for an entity', 400)

        nodelabels = en['labels']
        nodeprops = en['properties']
        nodeprops['crawl_en_id'] = 'en_'+tokenid+'_'+taskname+'_'+str(nodeid)
        nodes[nodeid] = {'labels':nodelabels,'properties':nodeprops}

    required_reldict_props = ['label','properties','start_entity','end_entity','bidirectional','id']
    reserved_rel_props = ['crawl_rel_id','resolvedWithRELID','taskname','token','_token','workname','date','time','resolvedDate','resolvedAgainst','verifiedBy','resolvedBy','verifiedDate','update','lastUpdatedBy','lastUpdatedOn']
    required_rel_props = [] ##inside entity['properties']

    for rel in relations:

        for prop in required_reldict_props:
            if not prop in rel:
                return error_helper(str(prop)+' required attribute missing for a relation', 400)

        linkid = rel['id']
        if linkid in links:
            return error_helper('id repeated under relations',400)
        
        linklabel = rel['label']

        if len(linklabel)<3:
            return error_helper('Label too short for a relation', 400)
        
        bidirectional = rel['bidirectional']

        print 'bbbbbb '+bidirectional
        if bidirectional!='yes' and bidirectional!='no':
            return error_helper('bidirectional not yes/no for a for a relation', 400)

        for prop in required_rel_props:
            if not prop in rel['properties']:
                return error_helper(str(prop)+' required property missing for a relation', 400)

        for prop in reserved_rel_props:
            if prop in rel['properties']:
                return error_helper(str(prop)+' reserved property not allowed explicitly for a relation', 400)

        linkprops = rel['properties']
        startnode = 'en_'+tokenid+'_'+taskname+'_'+str(rel['start_entity'])
        endnode = 'en_'+tokenid+'_'+taskname+'_'+str(rel['end_entity'])
        linkprops['crawl_rel_id'] = 'rel_'+tokenid+'_'+taskname+'_'+str(linkid)
        linkprops['bidirectional'] = bidirectional

        
        
        links[linkid] = {'label':linklabel,'properties':linkprops,'start_entity':startnode, 'end_entity':endnode}        
        

    posted, msg = postSubGraph(getGraph(), nodes, links, tokenid, taskname)
    if not posted:
        return error_helper(msg, 400)

    subgraph['entities'] = nodes
    subgraph['relations'] = links


    data = jsonify(subgraph)

    return data, 201 ## 201 is for creation!
    ##Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"taskname":"wow","description":"Some values!"}' http://localhost:5000/newlinks/pushlinked/?_token=NexusToken2