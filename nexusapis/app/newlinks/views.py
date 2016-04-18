from app.newlinks import newlinks
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify

##Usage: http://localhost:5000/newlinks/randomrandom/?_token=NexusToken
## http://localhost:5000/newlinks/randomrandom?_token=NexusToken
@newlinks.route('/randomrandom/')
def show():
    return jsonify({'message':'randomrandom success'}), 200
    # resp = Response(response=jsonify({'message':'randomrandom'}), 
    #     status=200, 
    #     mimetype="application/json")
    # return(resp)

@newlinks.route('/')
def home():
    return jsonify({'message':'Token works!'}), 200
