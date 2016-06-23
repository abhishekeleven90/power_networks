from app import app
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from functools import wraps
from forms import RegisterationForm, LoginForm, form_error_helper
from dbwork import *
import smtplib
import socks
import hashlib
import pandas as pd
import peewee
#import gdb2csv as gd
#import search_query as sq

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            flash('Please login first to use this')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def home():
    return render_template("home.html", homeclass="active")

@app.route('/temp/')
def temp():
    return render_template("temp4.html")

@app.route('/login/',methods=["GET","POST"])
def login():
    '''
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '10.10.78.62', 3128)
    socks.wrapmodule(smtplib)
    server = smtplib.SMTP_SSL('smtp.gmail.com',port=465)
    #server = smtplib.SMTP('smtp.gmail.com',587)
    #server.starttls()
    server.login('abhishekeerie1234@gmail.com','')
    server.sendmail(fromaddr, toaddrs, msg)
    smtpObj.sendmail('abhishekeerie1234@gmail.com', ['abhiagar90@gmail.com'], 'New msg')
    server.quit()
    print "Successfully sent email"
    '''
    #TODO: check if temp.html works fine always
    if session.get('userid') >= 1:
        return render_template("temp.html", loginclass="active", signincss=False, temptext="Already logged in!")
    form = LoginForm()
    if form.validate_on_submit():
        try:
            from app.models.dbmodels.user import User
            userid = form.email.data
            password = form.password.data
            usr = User.getUser(userid=userid)

            if not usr.validateUser(password):
                raise Exception

            session['userid'] = usr.userid
            session['role'] = usr.role
            usr.setLastLogin()
            flash('Successfully logged in')
            print (session)
            return redirect('home')
        except Exception as e:
            import traceback
            print traceback.format_exc()
            print repr(e)
            flash('Details do not match')
    else:
        form_error_helper(form)
    return render_template("login2.html", loginclass="active", signincss=False, form = form)

@app.route('/logout/',methods=["GET","POST"])
def logout():
    if not session.get('userid'):
            return render_template("temp.html", loginclass="active", signincss=False, temptext="Please log in first!")
    session.clear()
    return render_template("logout.html", loginclass="active", signincss=False, temptext="Successfully logged out!")

#get to land first on signup page, post to actually sign up
@app.route('/signup/', methods=["GET", "POST"])
def signup():
    from app.models.dbmodels.user import User
    form = RegisterationForm()
    if form.validate_on_submit():
        flash('Signup details valid')
        name = form.name.data
        password = form.password.data
        userid = form.email.data
        usr = User(userid=userid, password=password, name=name)
        usr.insert()
        flash('Successfully signed up. Login to continue!')

        return redirect(url_for('.home'))
    else:
        form_error_helper(form)
    return render_template("signup.html", signupclass="active", signincss=True, form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", homeclass="active", errortext="Sorry, the page does not exist.")

@app.errorhandler(403)
def not_permitted(e):
    return render_template("error.html", homeclass="active", errortext="Sorry, you are not permitted to see this.")

@app.route('/temp6/')
@login_required
@role_required('admin')
def temp6():
    nayaperson = Person.create(name='nayaperson')
    naya_kitty = Pet.create(ownerid=nayaperson, type='cat')
    toflash = ''
    for person in Person.select():
        toflash = toflash + (str(person.id)+" "+person.name) + "\n\r"
    flash(toflash)
    return render_template("temp.html", homeclass="active", temptext=str(nayaperson.id)+" "
        +str(naya_kitty.id))

@app.route('/search/', methods = ['GET','POST'])
def search():

    name = request.form.get('query')
    if name is None or name == '':
        return render_template("search_results.html", uuids= [], name='', nodes = [], labelstr ='', keywordstr = '', numrows = 10)

    rows = request.form.get('rows')

    if rows is None or rows == '':
        rows = 10

    ##TODO: more validation for labels
    labelstr = request.form.get('labels')

    labels = ''
    if labelstr is None or labelstr =='':
        labels = ['entity']
        labelstr = 'entity'
    else:
        labels = labelstr.split(' ')

    #TODO: more validation for keywords
    keywordstr = request.form.get('keywords')
    keywords = ''
    if keywordstr is None or keywordstr =='':
        keywordstr = ''
        keywords = []
    else:
        keywords = keywordstr.split(' ')


    # print keywords
    # print name, rows, labels, keywords
    from app.solr.searchsolr_phonetic import get_uuids
    uuids = get_uuids(name=name, labels=labels, rows=rows, aliases = [name], keywords = keywords)
    from app.models.graphmodels.graphdb import CoreGraphDB
    coredb = CoreGraphDB()
    nodes = coredb.getNodeListCore(uuids)
    return render_template("search_results.html", uuids= uuids, name=name, nodes = nodes, labelstr =labelstr, keywordstr = keywordstr, numrows = rows)


#Moved to forms.py
'''def form_error_helper(form):
    for field, errors in form.errors.items():
           for error in errors:
               flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))
'''

#show the page about this entity
#show an edit button on that page if the user is logged in, or route to log in page, how to remember?
#the int works fine here
#history/last edited??
@app.route('/entity/<int:uuid>/')
def readEntity(uuid):
    ##read about the entity from the graph db
    ##get that info and convert into presentable format
    ##show that info
    ## show the graph and connections in pble format? pble = presentatble
    from app.models.graphmodels.graphdb import CoreGraphDB
    core = CoreGraphDB()
    node = core.entity(uuid)
    outrels = core.getDirectlyConnectedRelations('uuid', str(uuid), uniquelabel='entity', isIDString = False,outgoing=True)
    inrels = core.getDirectlyConnectedRelations('uuid', str(uuid), uniquelabel='entity', isIDString = False,outgoing=False)
    #3missing is how to better represent it online
    return render_template("entity_read.html",
        homeclass="active",
        uuid=str(uuid),
        entity=str(node),node=node,outrels=outrels,inrels=inrels)


# @app.route('/changes/<int:changeid>/',defaults={'uuid': None},  methods=["GET","POST"])
@app.route('/changes/<string:type>/<string:id>/',defaults={'name': None, 'subtype': None}, methods=["GET","POST"])
@app.route('/changes/<string:type>/<string:subtype>/<string:name>/<string:id>/', methods=["GET","POST"])
def changes(type, id, name, subtype):
    ##show all changes for this changeid
    '''
        type=change -- id is changeid
        type=user -- id is userid

        for all above two subtype is None automatically
        for all above two name is None automatically

        type=relation, id is relid
            if subtype not None:
                subtype=prop, name is prop's name
                subtype=label, name is label's name

        type=entity, id is uuid
            if subtype not None:
                subtype=prop, name is prop's name
                subtype=label, name is label's name
    '''
    ##TODO:pagination?? afterwards will see
    ## http://127.0.0.1:5001/changes/change/345/
    if type == "change":
        ##TODO show change table
        id = int(id)  # convert to string
        from app.models.dbmodels.change import ChangeItem
        chg = ChangeItem.getChangeItem(id).__dict__.copy()
        del chg['dbwrap']
        del chg['tablename']

        return render_template("changeid.html", changeid_entry=chg,
                               typestr='obj')

    ## http://127.0.0.1:5001/changes/user/545/

    print type
    if type == "user":
        from app.models.dbmodels.change import ChangeItem
        chgList = ChangeItem.getChangesUserId(id)
        return render_template("changeid.html", props=chgList,
                               prop_keys=chgList[0].keys(), typestr='list')

    ##
    if type == "entity" or type == "relation":
        from app.models.dbmodels.uuid import UuidLabels, UuidProps, UuidTable
        from app.models.dbmodels.relid import RelProps, RelLabels, RelIdTable

        id = int(id) ##convert to string
        if subtype is None:
            ## http://127.0.0.1:5001/changes/entity/345/
            ## http://127.0.0.1:5001/changes/relation/345/
            if type == "entity":
                obj = UuidTable.getUuid(id)
                ulList = UuidLabels.getUuidLabelsUUId(id)
                upList = UuidProps.getUuidPropsUUId(id)
                return render_template("uuid.html", uuid_entry=obj, labels=ulList,
                                       label_keys=ulList[0].keys(), props=upList,
                                       prop_keys=upList[0].keys())

            else:
                obj = RelIdTable.getRel(id)
                rlList = RelLabels.getRelLabelsRelId(id)
                rpList = RelProps.getRelPropsRelId(id)
                return render_template("relid.html", relid_entry=obj, labels=rlList,
                                       label_keys=rlList[0].keys(), props=rpList,
                                       prop_keys=rpList[0].keys())


        elif subtype=="label" or subtype=="prop":
            ## http://127.0.0.1:5001/changes/entity/label/politcian/345/
            ## http://127.0.0.1:5001/changes/entity/prop/name/345/
            ## TODO: take care of label or prop doesnt exist for the graph object
            return "change table being shown for %s, %s, %s, %s" %(type,subtype,name,id)

    abort(404)

#show the page about this relation
#show an edit button on that page if the user is logged in, or route to log in page, how to remember?
#the int works fine here
@app.route('/relation/<int:relid>/')
def readRelation(relid):
    ##read about the rel from the graph db
    ##get that info and convert into presentable format
    ##show that info
    ##should include a visualization too
    from app.models.graphmodels.graphdb import CoreGraphDB
    gg = CoreGraphDB()
    rel = gg.relation(relid)
    #missing is how to better represent it online
    return render_template("relation_read.html", homeclass="active",
        rel=rel);

@app.route('/hyperedgenode/<int:henid>/')
def readHyperEdgeNode(henid):
    ##read about the hyperedge node from the graph db
    ##get that info and convert into presentable format
    ##show that info
    ## show the graph and connections in pble format? pble = presentatble
    from app.models.graphmodels.graphdb import CoreGraphDB
    gg = CoreGraphDB()
    node = gg.hyperedgenode(henid)
    #3missing is how to better represent it online
    return render_template("entity_read.html",
        homeclass="active",
        uuid=str(uuid),
        entity=str(node),node=node)

##TODO: all three read functions can be confined in one i think and shouldn't be an issue but the file name would change for all

@app.route('/profile/')
def profile():
    return render_template("profile.html", homeclass="active")

@app.route('/connections/')
def conn():
    return render_template("connections.html", homeclass="active")

@app.route('/trial/')
def trial():

    from app.models.dbmodels.idtables import Entity, Link
    from app.models.graphmodels.graphdb import CoreGraphDB

    coredb = CoreGraphDB()

    results = coredb.graph.cypher.execute('match n return id(n)')

    for res in results:
        currid =  res[0]
        #print currid

        currnode = coredb.getNodeByInternalId(currid)

        #print currnode['uuid']

        en = Entity(currnode['name'])
        en.create()
        currnode['uuid'] = en.uuid
        print 'id: '+str(currid) + '; '+ 'uuid: '+str(currnode['uuid'])

        # currnode.push()

    return 'done'


@app.before_first_request
def background():
    #startBackGroundJob()
    return

def alarm(time, sched):
    from datetime import datetime, timedelta
    from app.models.graphmodels.graphdb import SelectionAlgoGraphDB
    from app.constants import CRAWl_JOB_INTERVAL


    gg = SelectionAlgoGraphDB()
    nodes, rels = gg.releaseLocks()
    if nodes!=0 or rels!=0:
        print('JOB! This job was scheduled at %s.' % time)
        print '('+str(nodes)+','+str(rels)+')' + 'crawl verifier locks released in this cycle'
    alarm_time = datetime.now() + timedelta(seconds=CRAWl_JOB_INTERVAL)

    sched.add_job(alarm, 'date', run_date=alarm_time, args=[datetime.now(), sched])

#def startBackGroundJob():
#    from apscheduler.schedulers.background import BackgroundScheduler
#    sched = BackgroundScheduler()
#    sched.start()
#    from datetime import datetime
#    alarm(datetime.now(),sched)
