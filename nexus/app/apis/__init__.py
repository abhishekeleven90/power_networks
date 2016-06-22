from flask import Blueprint, render_template, abort, g, session

apis = Blueprint('apis', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@apis.before_request
def before_request():
    # from app.constants import ROLE_MODERATOR
    # if session.get('role')<ROLE_MODERATOR:
    #     abort(403)
    ##TODO: user, token
    print 'apis hi!!!' ##this is like a wrapper inside a wrapper

@apis.after_request
def after_request(response):
    print "apis bye!!!"
    # print g.db ## this object exists!!
    return response

from app.apis import views
