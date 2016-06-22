from app import app
from flask import render_template, flash, redirect, session, g, request, url_for, abort, jsonify

##Usage: curl -i http://localhost:5000/
@app.route('/')
@app.route('/home/')
@app.route('/index/')
def home():
	print request
	print request.args.get('_token') ##if not using get will throw bad request error!
	print request.headers
	print request.data
	print request.json
	return jsonify({'message': 'Welcome to Power Nexus APIS'}), 200

##just a helper api, remove when time: TODO
@app.route('/security/')
def security():
	abort(403)

##just a helper api, rmeove when time: TODO
@app.route('/logout/', methods=['GET'])
def logout():
	session.clear()
	return jsonify({'message': 'Session cleared'}), 200



@app.route('/validjson/',methods=['POST'])
def validjson():
	print 'here'
	print request
	print request.headers
	print request.data
	print request.json
	# currdict = {}
	# currdict['emailid']  = 'abhi@gmail.com'
	# currdict['url'] = 'http://bit.ly'
	from werkzeug.datastructures import MultiDict
	from app.forms import URLForm
	formdata = MultiDict(mapping=request.json)
	form = URLForm(formdata, csrf_enabled=False)

	if form.validate():
		return jsonify({'message':'yes'}), 200

	else:
		# msg = ""
		# for prop in form:
		# 	print prop.name+" " +prop.data
		# 	msg = msg + str(prop.data) + " "
		#
		# # msg = msg + form.emailid.data+" "+form.password.data+" "+"no"
		# # msg = msg + str(form.emailid.errors)
		# # msg =  msg + str(form.password.errors)

		reply = {}
		reply['message'] = 'no'
		reply['erros'] = form.errors
		return jsonify(reply)

@app.route('/validjson2/',methods=['POST'])
def validjson2():
	print request.json
	# currdict = {}
	# currdict['emailid']  = 'abhi@gmail.com'
	# currdict['url'] = 'http://bit.ly'
	from werkzeug.datastructures import MultiDict
	from app.forms import EntityValidForm
	formdata = MultiDict(mapping=request.json)
	form = EntityValidForm(formdata, csrf_enabled=False)

	if form.validate():
		return jsonify({'message':'yes'}), 200

	else:
		reply = {}
		reply['message'] = 'no'
		reply['erros'] = form.errors
		return jsonify(reply)



##@app.errorhandler(404)
##def page_not_found(e):
##	return render_template("error.html", homeclass="active", errortext="Sorry, the page does not exist.")

##@app.errorhandler(403)
##def not_permitted(e):
##	return render_template("error.html", homeclass="active", errortext="Sorry, you are not permitted to see this.")
