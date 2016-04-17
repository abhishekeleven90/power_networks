from app import app
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify
from dbwork import *

##Usage: curl -i http://localhost:5000/
@app.route('/')
@app.route('/home/')
@app.route('/index/')
def home():
    return jsonify({'message': 'Welcome to Power Nexus APIS'}), 200


@app.route('/security')
def security():
    abort(403)


##@app.errorhandler(404)
##def page_not_found(e):
##    return render_template("error.html", homeclass="active", errortext="Sorry, the page does not exist.")

##@app.errorhandler(403)
##def not_permitted(e):
##    return render_template("error.html", homeclass="active", errortext="Sorry, you are not permitted to see this.")







