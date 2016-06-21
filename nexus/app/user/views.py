from app.user import user
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.forms import EditEntityForm, form_error_helper

@user.route('/')
def show():
	from app.models.dbmodels.user import User
	user = User.getUser(session['userid'])
	##!!PROV!!: call all changes made by this user
	##!!ELELV!!
	##show changes in view
	##also this profile can be shown to the amdin etc for elevate button
	return render_template("user_profile.html", user = user)


# # TODO: check if the ending forward slashes are there for all
# #  do it when checking
# @user.route('/editEntity/<int:uuid>/',methods=["GET","POST"])
# def editEntity(uuid):
# 	##fetch current details for now
# 	##show these current details
# 	##edit form of entity?
# 	##wait for moderation
#
# 	##for now lets just show the current text
# 	##and give a text area for updating the text
# 	##let the user update it
# 	##we will save both in a db
# 	##who to any moderator who logs in afterwards
# 	##who approves dispapproves --> and the change goes to the db
# 	##will save this to a log
#
# 	##TODO: UUIDS are not changeable for ever, make a check of that
#
#
# 	# delete a node with uuid and create a node
#
# 	from app.graphdb import *
# 	node = entity(uuid)
# 	entity = str(node)

# 	form = EditEntityForm()
# 	if form.validate_on_submit():
# 		try:
# 			newnodetext = form.new_entity.data
# 			newnodetext = newnodetext.strip()
# 			nayanode = deserializeNode(newnodetext)
# 			updatePrev(uuid,nayanode)
# 			flash(newnodetext)
# 			return redirect('entity/'+str(uuid))
# 		except Exception as e:
# 			print 'Exception'
# 			print e
# 			flash('Form not filled properly')
# 	else:
# 		form_error_helper(form)
# 	return render_template("edit_entity.html", homeclass="active",uuid=str(uuid), entity=entity, form=form)


##TODO: this code here is an experiment with wtf validation without actually getting data form a form
## do it when checking
@user.route('/temp/')
def temp():
	currdict = {}
	currdict['emailid']  = 'abhi@gmail.com'
	currdict['url'] = 'http://bit.ly'
	from werkzeug.datastructures import MultiDict
	from app.forms import URLForm
	formdata = MultiDict(mapping=currdict)
	form = URLForm(formdata, csrf_enabled=False)

	if form.validate():
		return "yes"

	else:
		# msg = ""
		# for prop in form:
		# 	print prop.name+" " +prop.data
		# 	msg = msg + str(prop.data) + " "
		#
		# # msg = msg + form.emailid.data+" "+form.password.data+" "+"no"
		# # msg = msg + str(form.emailid.errors)
		# # msg =  msg + str(form.password.errors)
		msg = ''
		msg =  msg + str(form.errors)
		return msg
	return render_template("temp.html", temptext='temp')

##to be done for bypassing csrf, but not req now
def mycustomvalid(form, dict):
	##but can be used when constructin isntance, csrf_enabled=False
	errors = []
	for prop in dict:
		for err in form[prop].errors:
			errors.append(err)
	return errors


def wikiHelper(kind, obj, objid, work):

	from app.models.graphmodels.graph_handle import GraphHandle
	# from py2neo import Node, Relationship
	gg = GraphHandle()

	copyobj = gg.coredb.copyObjectAsItIs(kind, obj)

	labels = diffLabelsNeeded(kind)

	needed = diffPropsNeeded(copyobj,kind=kind)
	##helps!!
	for prop in needed:
		copyobj[prop] = ''

	form = ''
	if kind=='relation':
		from app.forms import AddRelationForm
		form = AddRelationForm()

	if 'editForm' in request.form: ##life saviour line! ##editForm is the submit button!

		##TODO: remove uselsss flashes from here
		sourceurl = request.form.get('sourceurl')

		# print sourceurl
		# print len(sourceurl)
		flash(sourceurl)

		propnames = request.form.getlist('propname[]')
		propvals = request.form.getlist('propval[]')

		orignames = request.form.getlist('actualpropname[]')
		origvals = request.form.getlist('actualpropval[]')

		##will be empty if relation
		origlabels = request.form.getlist('origlabel[]')
		newlabels = request.form.getlist('newlabel[]')



		newobj = gg.coredb.copyObjectAsItIs(kind, copyobj)

		# ignore uuid
		# if props with same name again , consider later one
		# if
		flash(str(propnames)+ " ::::: " +str(propvals))
		newpropdict = {}
		ll = len(propnames)
		for i in range(ll):
			if (len(propnames[i].strip())>1):
				if (len(propvals[i].strip())>0):
					newpropdict[propnames[i]] = propvals[i]

		flash(str(orignames) + " :::::: " +str(origvals))
		#flash(str(needednames) +" :::::: "+str(neededvals))
		flash(str(newlabels))

		newlabelsnonempty = []
		for label in newlabels:
			if len(label.strip())>0:
				newlabelsnonempty.append(label.strip())

		newobj = gg.coredb.copyObjectAsItIs(kind, copyobj)

		ll = len(origvals)
		origpropdict = {}
		for i in range(ll):
			if (len(orignames[i].strip())>1):
				if (len(origvals[i].strip())>0): ##THOUGH HERE TOO WE HAVE KEEP HOLD ON '' name
					newobj[orignames[i].strip()] = origvals[i].strip()


		flag = False
		msg = ""

		if sourceurl is None or len(sourceurl)<10:
			msg = msg + 'sourceurl check again' +';;;'
			flag = True

		if kind=='node': ##THIS TAKES CARE OF NAME, very imp for add node
			if len(str(newobj['name']).strip())<3: ##TODO: name validation
				msg = msg + ' name property too short' +';;;'
				flag = True

		for prop in newpropdict: ##THIS WILL TAKE CARE OF UUID OR RELID
			if prop in newobj:
				msg = msg + ' Added a custom prop that has same name as in our required prop list' +';;;'
				flag = True

		if flag:
			flash(msg)
			return render_template('user_edit.html', sourceurl =sourceurl, obj = newobj, newpropdict=newpropdict, needed = needed, labels=labels, newlabels=newlabelsnonempty, kind=kind, objid=objid, form = form, work=work)

		else:

			nayaobj = gg.coredb.copyObjectAsItIs(kind, newobj)

			for label in newlabelsnonempty:
				nayaobj.labels.add(label)

			for prop in newpropdict:
				nayaobj[prop] = newpropdict[prop]

			for prop in newobj.properties:
				if len(str(newobj[prop]).strip())==0:
					nayaobj[prop]=None

			##adding MVP patch for wiki:
			from app.constants import MVPLIST
			for prop in MVPLIST:
				if prop in nayaobj:
					aliaslist = nayaobj[prop].split(',')
					nayaobj[prop] = []
					for alias in aliaslist:
						if len(str(alias))>0:
							nayaobj[prop].append(alias)

			###XXX:
			##jsonvalidatehelper
			##make a json TODO
			##validate json api call normal without token
			##whould give true
			#json object to be made at this point for this object remove uuid and stuff
			###and then validate that json using the code in api, when merge! TODO


			someobj = gg.wikiObjCreate(kind, nayaobj, session['userid'], sourceurl)

			flash(str(someobj))

			flash('Successfully pushed for moderation')

			if objid is not None:
				if kind=='node':
					return redirect(url_for('readEntity',uuid=objid))
				if kind =='relation':
					return redirect(url_for('readRelation',relid=objid))
			else:
				return redirect(url_for('home'))


	return render_template('user_edit.html', sourceurl='', obj  = copyobj, needed = needed,  labels=labels, kind=kind, objid=objid, form=form, work = work)



@user.route('/add/<string:kind>/',  defaults={'objid': None}, methods=["GET","POST"])
@user.route('/edit/<string:kind>/<int:objid>/', methods=["GET","POST"])
def edit(kind, objid):

	work = 'edit'
	if objid is None:
	 	work = 'add'


	##INFO: XXX:
	##even if you delete aliases and add only one value, it will take is a listld be no issue
	##comma seperated
	# livedin mvp, a prop will come for our mvp, assume something ##alsg se tab
	#
	# livedin a mvp prop will change to relation
	# bornin a prop will change to relation
	# diedin a prop will change to relation
	# aliases, livedin
	##also countries related to

	from app.models.graphmodels.graph_handle import GraphHandle
	from py2neo import Node, Relationship
	gg = GraphHandle()

	labels  = []

	obj = None

	if objid is not None:
		obj = gg.getOriginalCoreObject(kind, objid)
	else:
		if kind=='node':
			##by default giving entity label,
			##this is basically a hack
			##but if any more label, then have to have a pre page
			##as in relation
			obj=Node("entity")
		elif kind=="relation":

			from app.forms import AddRelationForm
			form = AddRelationForm()
			print request.method


			if form.validate_on_submit():

				starnodeid = form.startnodeid.data
				endnodeid = form.endnodeid.data
				reltype = form.reltype.data

				startnode = gg.getOriginalCoreObject('node',starnodeid)
				endnode = gg.getOriginalCoreObject('node', endnodeid)
				obj = Relationship(startnode, reltype, endnode)

				return wikiHelper(kind, obj, objid, work)
			else:
				form_error_helper(form)

			return render_template('user_add_object.html',form = form)

	## works awesome for node
	return wikiHelper(kind, obj, objid, work)

@user.route('/sub/<string:kind>/', methods=["GET","POST"])
def sub(kind):
	if not request.form:
		from py2neo import Graph, Node, Relationship
		obj = Node("entity",name='')
		return render_template("user_edit_object.html")
	return kind

@user.route('/history/<int:uuid>/<string:prop>/')
def history(uuid,prop):
	return render_template("temp.html", temptext=str(uuid)+' and prop '+prop)

def diffLabelsNeeded(kind):


	mains = ['person','list','organization']
	subperson = ['businessPerson','politician','mediaPerson','lawPerson','primeMinister','chiefMinister','governor','memberOfParliament']
	suborg = ['school','business','privateCompany','publicCompany','mediaOrganization','notForProfit','government','socialClub']
	networks = ['indian','foreign']
	nodelabels =  mains+subperson+suborg+networks


	rellabels = ['worksIn','memberOf','family','spouseof']

	if kind == 'node':
		return nodelabels
	else:
		return rellabels

def diffPropsNeeded(node, kind='node'):

		# for person
		# not for organization
		# not for list
		ans = []

		if kind== 'node':
			props1 = ['name','blurlb','bio','startdate','enddate','iscurrent','website']

			##if person
			props2 = []
			if 'person' in node.labels:
				props2 = ['firstname','lastname','middlename','namesuffix','nameprefix'] ##idea of legal name from fn, ln mn


			props3 = ['startplace', 'endplace']

			props = props1 +props2 +props3 ##all these are person props


			for prop in props:
				if prop not in node.properties:
					ans.append(prop)


		else:

			props = ['startdate','enddate','iscurrent']
			for prop in props:
				if prop not in node.properties:
					ans.append(prop)




		return ans
