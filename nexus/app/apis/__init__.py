from flask import Blueprint, render_template, abort, g, session, request, jsonify

apis = Blueprint('apis', __name__)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@apis.before_request
def before_request():

    from app.models.dbmodels.user import User
    userid = request.args.get('userid',None)
    token = request.args.get('token',None)
    flag = True
    retdict = {}
    retdict['error'] = 'Not authorized'
    ret = jsonify(retdict)
    # print userid
    # print token
    if userid is None or token is None:
        # print 'here'
        return ret, 403
    if not User.validateToken(userid=userid,token=token):
        return ret, 403
    print 'apis hi!!!' ##this is like a wrapper inside a wrapper

@apis.after_request
def after_request(response):
    print "apis bye!!!"
    # print g.db ## this object exists!!
    return response

from app.apis import views
