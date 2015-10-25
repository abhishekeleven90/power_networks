from flask import Blueprint, render_template, abort, g, session

admin = Blueprint('admin', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@admin.before_request
def before_request():
    if session.get('role')!=7:
        abort(403)
    print 'admin hi!!!' ##this is like a wrapper inside a wrapper

@admin.after_request
def after_request(response):
    print "admin bye!!!"
    print g.db ## this object exists!!
    return response   

from app.admin import views 

