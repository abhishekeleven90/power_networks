from app.user import user
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@user.route('/')
def show():
    return render_template("temp.html", homeclass="active", temptext='user')

@user.route('/diff')
def diff():
	import app.temp as t 
	graph = t.getGraph()
	old,naya = t.createNodes(graph)
	temp = str(old) + '<hr/>' + str(naya)
	return render_template("temp.html", homeclass="active", temptext=temp)