from app.newlinks import newlinks
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify
from utils_crawler import *

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
    
    if not 'taskname' in request.json:
        return error_helper("taskname not in json data", 400)

    if not 'description' in request.json:
        return error_helper("description not in json data", 400)

    if not 'fetchdate' in request.json:
        return error_helper("fetchdate not in json data", 400)

    if not 'sourceurls' in request.json:
        return error_helper("sourceurls not in json data", 400)

    taskname = request.json['taskname']

    ## MAJOR TODO!
    ## check for strings 
    ## validation checks: if task exists, 
    ## ids repeated in nodes in json and in actual 
    ## ids repeated in relations
    ## source_urls known in particular format
    ## fetch date in format
    ## labels not empty
    ## props allowed
    ## values all in strings or particular format?
    ## apis to add a new property in allowed dict with its description?
    ## check if ids are ints 
    ## check if nodeid already exists in db, or relid


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

    for en in entities:
        #print entities[en]
        nodeid = en['id']
        if nodeid in nodes:
            return error_helper('id repeated under entities',400)
        
        if not 'labels' in en:
            return error_helper('Labels list missing for an entity', 400)
        if not len(en['labels'])>0:
            return error_helper('Labels list empty for an entity', 400)
        if not 'properties' in en:
            return error_helper('Properties map missing for an entity', 400)
        if not 'name' in en['properties']:
            return error_helper('Name property missing for an entity', 400)
        
        nodelabels = en['labels']
        nodeprops = en['properties']
        nodes[nodeid] = {'crawl_en_id':'en_'+tokenid+'_'+taskname+'_'+str(nodeid), 'labels':nodelabels,'properties':nodeprops}

    for rel in relations:
        linkid = rel['id']
        if linkid in links:
            return error_helper('id repeated under relations',400)
        
        if not 'label' in rel:
            return error_helper('Label missing for a relation', 400)
        linklabel = rel['label']

        if len(linklabel)<3:
            return error_helper('Label too short for a relation', 400)
        
        if not 'properties' in rel:
            return error_helper('Properties map missing for a relation', 400)
        linkprops = rel['properties']

        if not 'start_entity' in rel:
            return error_helper('Start entity reference missing for a relation', 400)
        starnode = rel['start_entity']
        
        if not 'end_entity' in rel:
            return error_helper('End entity reference missing for a relation', 400)
        endnode = rel['end_entity']
        

        if not 'bidirectional' in rel:
            return error_helper('Bidirecional property missing for a relation', 400)
        bidirectional = rel['bidirectional']

        print 'bbbbbb '+bidirectional
        if bidirectional!='yes' and bidirectional!='no':
            return error_helper('bidirectional not yes/no for a for a relation', 400)
        
        links[linkid] = {'crawl_rel_id':'rel_'+tokenid+'_'+taskname+'_'+str(linkid), 'label':linklabel,'properties':linkprops}        
        

    subgraph['entities'] = nodes
    subgraph['relations'] = links

    data = jsonify(subgraph)
    
    return data, 201
    ##Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"taskname":"wow","description":"Some values!"}' http://localhost:5000/newlinks/pushlinked/?_token=NexusToken2