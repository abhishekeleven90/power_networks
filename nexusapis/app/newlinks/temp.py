##TODO: can be handled by session for now, then persistence can be brought in picture
##Usage: http://localhost:5000/newlinks/startwork/?_token=NexusToken2&workname=wow5

##TODO: GET or PUSH??? 
@newlinks.route('/startwork/', methods=['POST'])
def startWork():
    ##against the token number in session dict
    ##save a dict with workname given
    ##no startwork can begin till this token dict in session
    ##endwork will remove the token dict!
    ##TODO: remove this work from session after an hour

    ##two args needed here thus!
    if session.get(request.args.get('_token'),None) is not None:
        return jsonify({'message': 'startwork: Already in progress, use endwork first'}), 400
    
    timenow = getTimeNow()
    
    workname = request.args.get('workname',None)
    tokenid = request.args.get('_token')

    if workname is None:
        return jsonify({'message': 'startwork: Cannot start, no workname given to start'}), 400    

    to_save_dict = {}
    to_save_dict['_token'] = tokenid ## no sense, butfor better http response
    to_save_dict['workname'] = workname
    to_save_dict['starttime'] = timenow
    to_save_dict['status'] = 'Active'

    session[tokenid] = to_save_dict
    print session[tokenid]
    return jsonify(to_save_dict), 200

##Usage: http://localhost:5000/newlinks/endwork/?_token=NexusToken2
@newlinks.route('/endwork/', methods=['PUT'])
def endWork():

    ##only one arg needed here!

    if session.get(request.args.get('_token'),None) is None:
        return jsonify({'message': 'endwork: No work against your token in progress, use startwork first'}), 400

    timenow = getTimeNow()

    tokenid = request.args.get('_token')
    popped_obj = session.pop(tokenid)
    popped_obj['endtime'] = timenow
    popped_obj['status'] = 'Ended' 
    
    return jsonify(popped_obj), 200


##Usage: http://localhost:5000/newlinks/currwork/?_token=NexusToken2
@newlinks.route('/currwork/', methods=['GET'])
def currwork():

    ##only one arg needed here!

    tokenid = request.args.get('_token')
    currwork = session.get(tokenid,None)

    if currwork is None:
        return jsonify({'message': 'currwork: No work against your token in progress'}), 200

    return jsonify(currwork), 200

    ##TODO: status of all previous works, etc.


'''To use taskname as: _taskID, _tokenID, _resolvedWithUUID'''
##TODO: taskname testing left!
##TODO: will have to filter out these properties when in UX work!
##TODO: do the same with relations!

##Q1
'''start n = node(*) 
match (n)--(c)
return n, count(*) as connections
order by connections desc limit 1'''


'''MATCH (n)
WITH n
WHERE rand()<0.5 return n limit 1'''

'''http://neo4j.com/docs/stable/query-where.html'''

##Q2
##Seems to be correct! Have to test!
'''start c = node(*) 
match (n)--(c)
where exists(n.__resolvedwithUUID)
return c, count(*) as connections
order by connections desc limit 1'''

#Tested with:
'''create (n:person {name:'Abhishek Agarwal 3',__resolvedwithuuid:'1111'}), 
(p:person {name:'Ayushi Agarwal 3'}), 
(z:person {name: 'Alok Agarwal 3'}), n-[:sibling]->p, p-[:daughterOf]->z return n,p,z'''


'''start n = node(*) 
match (n)--(c)
where not exists(n.__resolvedwithUUID)
return n, count(*) as connections
order by connections desc limit 1'''


##Use Q2 and if no result use Q1


##TODO: to ask if workname to be also used?

def nothing():
    pass