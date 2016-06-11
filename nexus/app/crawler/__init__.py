from flask import Blueprint, render_template, abort, g, session

crawler = Blueprint('crawler', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@crawler.before_request
def before_request():

    print 'AAYA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

#    if session.get('role')<2:
#        abort(403)
    print 'crawler hi!!!' ##this is like a wrapper inside a wrapper

@crawler.after_request
def after_request(response):
    print "crawler bye!!!"
    print g.db ## this object exists!!
    return response   

from app.crawler import views
