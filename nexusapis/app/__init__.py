from flask import Flask, g, jsonify
from newlinks import newlinks
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

## Code from here: http://flask.pocoo.org/snippets/83/ ##

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)

##DON'T ADD A FORWARD SLASH AFTER GUEST WILL CREATE A PROBLEM
app.register_blueprint(newlinks, url_prefix='/newlinks')

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
    print 'power nexus apis hi'
    g.db = dbwork.dbobject()
    g.db.connect()
    g.user = None ##Session related
    ##adding for neo4j graph

@app.after_request
def after_request(response):
    print 'power nexus apis bye'
    g.db.close()
    return response

from app import views