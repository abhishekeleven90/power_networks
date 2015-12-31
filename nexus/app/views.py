from app import app
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from functools import wraps
from forms import RegisterationForm, LoginForm
from dbwork import *
import smtplib
import socks
import hashlib
import pandas as pd
import peewee
import gdb2csv as gd
import search_query as sq
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

@app.route('/search/')
def search():
    query = request.args.get('query')
    labs = ["Party","Politician"]
    thres = [0.6,0.6]
    #for lab in labs:
    #    df = gcd.get_gdb_entity(query,lab) #check party name
    #    df_html = df.to_html(classes="table")
    #    if not df.empty:
    #        df_list.append(df_html)
    #        table_titles.append(lab)
    df_list,table_titles = gd.get_gdb_entity(query,labs,thres)
    print "Length of table titles-{}".format(len(table_titles))
    return render_template("search.html",table_title=table_titles,df_list = df_list,n_results = len(table_titles))



def get_current_user_role():
    return 'admin'

def form_error_helper(form):
    for field, errors in form.errors.items():
           for error in errors:
               flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))


'''work during extension'''
'''it's offciial we have uuids for nodes and relids for relation, not uniform??'''
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
    from graphdb import *
    node = entity(uuid)
    #3missing is how to better represent it online
    return render_template("temp.html", homeclass="active", temptext='Entity: ' +str(uuid)+"<br>"+str(node))

#show the page about this relation
#show an edit button on that page if the user is logged in, or route to log in page, how to remember?
#the int works fine here
@app.route('/relation/<int:relid>/')
def readRelation(relid):
    ##read about the rel from the graph db
    ##get that info and convert into presentable format
    ##show that info
    ##should include a visualization too
    from graphdb import *
    rel = relation(relid)
    #missing is how to better represent it online
    return render_template("temp.html", homeclass="active", temptext='Relation: ' +str(relid)+"<br>"+str(rel))






