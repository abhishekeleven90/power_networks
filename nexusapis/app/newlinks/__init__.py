from flask import Blueprint, render_template, abort, g, session, request

newlinks = Blueprint('newlinks', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@newlinks.before_request
def before_request():
    print 'newlinks hi!!!' ##this is like a wrapper inside a wrapper
    ##no need of token here
    # from utils_crawler import isValidToken
    # if not isValidToken(request.args.get('_token', ''),2):
        # abort(403)
    print 'newlinks hi2222!!!' ##this is like a wrapper inside a wrapper

@newlinks.after_request
def after_request(response):
    print "new links apis bye!!!"
    #print g.db ## this object exists!!
    return response

from app.newlinks import views
