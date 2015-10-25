from flask import Blueprint, render_template, abort, g, session

guest = Blueprint('guest', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@guest.before_request
def before_request():
    print 'guest hi!!!' ##this is like a wrapper inside a wrapper

@guest.after_request
def after_request(response):
    print "guest bye!!!"
    print g.db ## this object exists!!
    return response   

from app.guest import views 

