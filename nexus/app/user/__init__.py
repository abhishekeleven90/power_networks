from flask import Blueprint, render_template, abort, g, session

user = Blueprint('user', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@user.before_request
def before_request():
    from app.constants import ROLE_USER
    if session.get('role')<ROLE_USER:
        abort(403)
    print 'user hi!!!' ##this is like a wrapper inside a wrapper

@user.after_request
def after_request(response):
    print "user bye!!!"
    print g.db ## this object exists!!
    return response   

from app.user import views 

