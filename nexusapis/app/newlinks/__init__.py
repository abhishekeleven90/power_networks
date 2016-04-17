from flask import Blueprint, render_template, abort, g, session

newlinks = Blueprint('newlinks', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@newlinks.before_request
def before_request():
    ##if session.get('role')<2:
    ##    abort(403)
    print 'newlinks hi!!!' ##this is like a wrapper inside a wrapper

@newlinks.after_request
def after_request(response):
    print "new links apis bye!!!"
    print g.db ## this object exists!!
    return response   

from app.newlinks import views 

