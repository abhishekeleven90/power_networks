from app.newlinks import newlinks
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify

@newlinks.route('/randomrandom')
def show():
    return jsonify({'message':'randomrandom'}), 200
    # resp = Response(response=jsonify({'message':'randomrandom'}), 
    #     status=200, 
    #     mimetype="application/json")
    # return(resp)