from flask import Flask, g
from guest import guest

app = Flask(__name__)
app.register_blueprint(guest, url_prefix='/guest')
app.config.from_object('config')


from peewee import *
from dbwork import *


# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    ##you can any way handle all the session here
    ##you can keep a dict of route urls
    ##you need to get which url from some custom object flask may provide
    ##raise permission denied error
    g.db = dbwork.dbobject()
    g.db.connect()
    g.user = None ##Session related

@app.after_request
def after_request(response):
    g.db.close()
    return response

from app import views

