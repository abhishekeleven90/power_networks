from flask import Blueprint, render_template, abort, g, session

mod = Blueprint('mod', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@mod.before_request
def before_request():
    from app.constants import ROLE_MODERATOR
    if session.get('role')<ROLE_MODERATOR:
        abort(403)
    print 'mod hi!!!' ##this is like a wrapper inside a wrapper

@mod.after_request
def after_request(response):
    print "mod bye!!!"
    print g.db ## this object exists!!
    return response   

from app.mod import views 

