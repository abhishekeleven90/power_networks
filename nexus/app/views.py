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
    if session.get('userid')>=1:
        return render_template("temp.html", loginclass="active", signincss=False, temptext="Already logged in!")
    form = LoginForm()
    if form.validate_on_submit():
        try:
            someobj = Users.get(Users.userid == form.emailid.data, Users.password == 
                hashlib.md5(form.password.data).hexdigest())
            session['userid']=someobj.userid
            session['role']=someobj.role
            flash('Successfully logged in')
            print session
            return redirect('home')
        except:
            flash('Details do not match')
    else:
        form_error_helper(form) 
    return render_template("login2.html", loginclass="active", signincss=False, form = form)

@app.route('/logout/',methods=["GET","POST"])
def logout():
    if not session.get('userid'):
            return render_template("temp.html", loginclass="active", signincss=False, temptext="Please log in first!")
    session.clear()
    return render_template("temp.html", loginclass="active", signincss=False, temptext="Successfully logged out!")

#get to land first on signup page, post to actually sign up
@app.route('/signup/', methods=["GET","POST"]) 
def signup():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash('Signup details valid')
        return redirect('home')
    else:
        form_error_helper(form)
    return render_template("signup.html", signupclass="active", signincss=True, form=form) 

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", homeclass="active", errortext="Sorry, the page does not exist.")

@app.errorhandler(403)
def not_permitted(e):
    return render_template("error.html", homeclass="active", errortext="Sorry, you are not permitted to see this.")

@app.route('/temp/')
@login_required
@role_required('admin')
def temp():
    nayaperson = Person.create(name='nayaperson')
    naya_kitty = Pet.create(ownerid=nayaperson, type='cat')
    toflash = ''
    for person in Person.select():
        toflash = toflash + (str(person.id)+" "+person.name) + "\n\r"
    flash(toflash)
    return render_template("temp.html", homeclass="active", temptext=str(nayaperson.id)+" "
        +str(naya_kitty.id))

@app.route('/search/', methods = ['POST'])
def search():
    print 'inside method rrrrrrrrrrrrrrrrrrrrrr'
    name = request.form.get('query')
    rows = request.form.get('rows')
    labels = request.form.get('labels')
    keywords = request.form.get('keywords')
    print name, rows, labels, keywords
    from app.solr.searchsolr_phonetic import get_uuids
    uuids = get_uuids(name=name, rows=10, aliases = [name], keywords = [])
    return render_template("search_results.html", uuids= uuids, name=name)


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
    gg = CoreGraphDB()
    node = gg.entity(uuid)
    #3missing is how to better represent it online
    return render_template("entity_read.html", 
        homeclass="active", 
        uuid=str(uuid),
        entity=str(node),node=node)

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









