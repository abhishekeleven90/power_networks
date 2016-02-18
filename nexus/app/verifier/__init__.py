from flask import Blueprint, render_template, abort, g, session

verifier = Blueprint('verifier', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@verifier.before_request
def before_request():
    print 'AAYA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    if session.get('role')<3:
        abort(403)
    print 'verifier hi!!!' ##this is like a wrapper inside a wrapper

@verifier.after_request
def after_request(response):
    print "verifier bye!!!"
    print g.db ## this object exists!!
    return response   

from app.verifier import views 

