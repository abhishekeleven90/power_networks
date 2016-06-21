from app.guest import guest
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.solr.SolrIndex import *

@guest.route('/')
def show():
    import hashlib
    text = hashlib.md5("yoyo").hexdigest()
    return render_template("temp.html", homeclass="active", temptext=text)

@guest.route('/temp2/')
def temp2():
    from app.models.dbmodels.index_entities import Entity
    print 'should work fine'
    #Entity.del_all_entities()
    #en = Entity(4, 'Kapil', 'person,politician', 'Kapil, Thakkar', 'gujrat iit mumbai')
    #rows = en.insertEntity()
    #en.name = 'Amartya'
    #en.updateEntity()
    en2= Entity()
    en2.getEntity(4)
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext ='You are here '+en2.name+' '+en2.labels)

@guest.route('/uuid/<int:id>/')
def uuid(id):
    print ''
    from app.models.dbmodels.uuid import UuidTable, UuidLabels, UuidProps
    #TODO - get uuid props 
    uuid_props_list = UuidProps.getUuidPropsUUId(id)
    #TODO - get uuid labels
    uuid_lab_list = UuidLabels.getUuidLabelsUUId(id)
    #TODO - get uuid table ... all sorted by cid
    u = UuidTable.getUuid(id).__dict__.copy()
    del u['dbwrap']
    del u['tablename']
    #TODO - send all data to uuid.html

    return render_template("uuid.html", props=uuid_props_list,
            prop_keys=uuid_props_list[0].keys(), labels=uuid_lab_list,
            label_keys=uuid_lab_list[0].keys(), uuid_entry=u)

@guest.route('/relid/<int:id>/<string:label>/<string:propname>/<string:newpropvalue>/')
@guest.route('/relid/<int:id>/')
def relid(id, label=None, propname=None, newpropvalue=None):
    print 'in relid'
    from app.models.dbmodels.relid import RelIdTable, RelLabels, RelProps

    if label is None or propname is None or newpropvalue is None:
        relid_props_list = RelProps.getRelPropsRelId(id)
        relid_lab_list = RelLabels.getRelLabelsRelId(id)
    else:
        relid_props_list = RelProps.getRelByPropRelId(propname, newpropvalue, id)
        relid_lab_list = RelLabels.getRelByLabelRelId(label, id)

    u = RelIdTable.getRel(id).__dict__.copy()
    del u['dbwrap']
    del u['tablename']
    
    return render_template("relid.html", temptext='You are here ',
                           props=relid_props_list, labels=relid_lab_list, relid_entry=u,
                           label_keys=relid_lab_list[0].keys(),
                           prop_keys=relid_props_list[0].keys())


@guest.route('/changeid/<int:id>/')
def changeid(id):
    print 'in changeid'
    from app.models.dbmodels.change import ChangeItem
    #TODO - get changeid table ... all sorted by cid
    u = ChangeItem.getChangeItem(id).__dict__.copy()
    #TODO - send all data to changeid.html
    del u['dbwrap']
    del u['tablename']

    return render_template("changeid.html", temptext='You are here ',
                            changeid_entry=u)


@guest.route('/rel/')
def rel():
    #First check reltable
    print 'should work fine'
    from app.models.dbmodels.relid import RelIdTable, RelLabels, RelProps
    #r = RelIdTable(1111111, reltype='works_in', startuuid = 10, enduuid=2)
    #r.create()
    #r2 = RelIdTable.getRel(1111111)
    #r2.startuuid = 1
    #r2.reltype = 'jingalala'
    #r2.update('all')

    #Second check rellabels
    ##TODO:
    r = RelLabels(changeid=5, relid=123, label='worksin', changetype=1)
    r.create()


    #r2 = RelLabels(changeid=2, relid=1111111, label='aa', changetype=1)
    #r2.create()
    #r3 = RelLabels.getRelLabels(2)
    #print r3

    #Last, check relprops ##TODO:
    # r = RelProps(changeid=5, relid=87587, propname='startDate',newpropvalue='23 August 1990', changetype=1)
    # r.create()


    # r2 = RelProps(changeid=2, relid=1111111, propname='mama',
    #               oldpropvalue='ert', newpropvalue='ort', changetype=1)
    # r2.create()
    # r3 = RelProps.getRelProps(2)
    # print r3

    return render_template("temp.html", homeclass="active", temptext='You are here ' + str(r))

@guest.route('/user/')
def user():

    from app.models.dbmodels.user import User
    usr = User(userid = 'abhi10@gmail.com', password = 'yoyo', role = 7, keyEnabled =1)
    usr.insert()
    flash(usr.userid)

    from app.models.dbmodels.tasks import Tasks, Taskusers
    task = Tasks(ownerid = usr.userid, name = 'Wiki Task', description = 'Wiki Task Description',iscrawled=0)
    task.create()
    flash(task.taskid)

    tuser = Taskusers(taskid=task.taskid, userid=usr.userid)
    flash('numrows for: taskusers: '+str(tuser.create()))


    # usr2 = User('abhi9.com', 'yoyo',3)
    # usr2.insert()
    # usr2.password = 'wewrerw'
    # usr2.update('password')
    # print usr2.validateUser('yummytummy')
    # usr2.role = 3
    # usr2.keyEnabled = 1
    # usr2.update('all')

    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext='No problem')

@guest.route('/tasks/')
def tasks():
    from app.models.dbmodels.tasks import Tasks, Taskusers, Tasklog
    print 'should work fine'
    ## Tasks class
    #task = Tasks('abhi1@gmail.com', 'yummytummy', 'yummytummydesc')
    #task.create()
    #task2 = Tasks('abhi7@gmail.com', 'zzzzzz')
    #task2.create()
    #print task2.taskid
    #task2.name = 'abhishekzzzz'
    #task2.description = 'new desc'
    #task2.update('all')
    #task2.description = 'more new desc'
    #task2.update('description')
    #task = Tasks.getTask(6)
    #print task.ownerid

    ## Taskusers class
    tuser = Taskusers(7, 'abhi7@gmail.com')
    tuser.create()

    ## Tasklogs class
    #tlog = Tasklog(9, 'abhishek', 'hifive', 'fatafati')
    #tlog.create()
    #tlog = Tasklog.getTasklog('abhishek', 9)
    #print tlog.description

    tusr = Taskusers(taskid=7)
    print tusr.getListFromDB('taskid')
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext='You are here')

@guest.route('/changeitem/')
def changeitem():
    from app.models.dbmodels.change import ChangeItem
    from app.utils.commonutils import Utils
    utils = Utils()
    fetchdate = utils.getCurrentDateTime()
    pushdate = utils.getCurrentDateTime()
    verifydate = utils.getCurrentDateTime()
    chg = ChangeItem(1, pushedby='abhi2@gmail.com', verifiedby=session['userid'], sourceurl='http://wikipedia.com', fetchdate=fetchdate, pushdate=pushdate, verifydate = verifydate)
    chg.insert()
    flash(chg.changeid)
    #chg2 = ChangeItem.getChangeItem(2)
    #print chg2
    #print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext='You are here ' + str(chg))



@guest.route('/temp3/')
def temp3():
    from app.utils.locprocess import getCityState
    (city,state) = getCityState('pondicherry')
    return render_template("temp.html", homeclass="active", temptext=city+' '+state)

@guest.route('/viz/', methods=['GET', 'POST'])
def viz():
    ##get cypher from request.args['cypher']

    ## use constant variables

    ##cypher variable is the one having query
    ##task 1 validate if query is read query - at start assume the query is valid

    ##### any validation function can be moved to graphdb.py later to see if the query is read or not.
    ##### use cypher card  : http://neo4j.com/docs/cypher-refcard/current/
    #####  CREATE, MERGE, DELETE, REMOVE, SET, INDEX, LOAD, LOAD CSV, CONSTRAINT, any case
    ##### nodes return, mandatory

    ##task 2 fecth the results of the query
    ##task 3 show on viz.html or something

    ##to decide: post or not?
    from app.utils.validate_cypher import isValidCypher

    cypher = ''
    if request.form:
        cypher = request.form.get('query')
    else:
        cypher = request.args['query']
    print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqueeeeeeeeeeeerrry'
    print cypher

    from app.constants import CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD, CORE_GRAPH_PORT, CORE_GRAPH_USER

    ## TODO: constants
    if isValidCypher(cypher):
        return render_template("viz2.html", homeclass="active", temptext=cypher,
            CORE_GRAPH_HOST =CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD = CORE_GRAPH_PASSWORD,
            CORE_GRAPH_PORT = CORE_GRAPH_PORT, CORE_GRAPH_USER = CORE_GRAPH_USER)
    else:
        flash('Invalid query')
        return render_template("viz2.html", homeclass="active", temptext='',
            CORE_GRAPH_HOST =CORE_GRAPH_HOST, CORE_GRAPH_PASSWORD = CORE_GRAPH_PASSWORD,
            CORE_GRAPH_PORT = CORE_GRAPH_PORT, CORE_GRAPH_USER = CORE_GRAPH_USER)

@guest.route('/temp4/')
def solr():
    delete_index()
    full_import()
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext = 'You are here')
