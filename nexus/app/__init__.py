from flask import Flask, g
from guest import guest
from admin import admin
from user import user
from mod import mod
from verifier import verifier

app = Flask(__name__)

##DON'T ADD A FORWARD SLASH AFTER GUEST WILL CREATE A PROBLEM
app.register_blueprint(guest, url_prefix='/guest')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(mod, url_prefix='/mod')
app.register_blueprint(verifier, url_prefix='/verifier')

app.config.from_object('config')

from peewee import *
from dbwork import *


# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    ##you can any way handle all the session here
    ##you can keep a dict of route urls
    ##you need to get which url from some custom object flask may provide
    ##raise permission denied error
    print 'app hi'
    g.db = dbwork.dbobject()
    g.db.connect()
    g.user = None ##Session related
    ##adding for neo4j graph

@app.after_request
def after_request(response):
    print 'app bye'
    g.db.close()
    return response

from app import views

