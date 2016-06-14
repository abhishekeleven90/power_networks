from app.user import user
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.forms import EditEntityForm, form_error_helper

@user.route('/')
def show():
	from app.models.dbmodels.user import User
	user = User.getUser(session['userid'])
	return render_template("user_profile.html", user = user)

##TODO: check if the ending forward slashes are there for all
## do it when checking
@user.route('/editEntity/<int:uuid>/',methods=["GET","POST"])
def editEntity(uuid):
	##fetch current details for now
	##show these current details
	##edit form of entity?
	##wait for moderation

	##for now lets just show the current text
	##and give a text area for updating the text
	##let the user update it
	##we will save both in a db
	##who to any moderator who logs in afterwards
	##who approves dispapproves --> and the change goes to the db
	##will save this to a log

	##TODO: UUIDS are not changeable for ever, make a check of that


	# delete a node with uuid and create a node 

	from app.graphdb import *
	node = entity(uuid)
	entity = str(node)

	form = EditEntityForm()
	if form.validate_on_submit():
		try:
			newnodetext = form.new_entity.data
			newnodetext = newnodetext.strip()
			nayanode = deserializeNode(newnodetext)
			updatePrev(uuid,nayanode)
			flash(newnodetext)
			return redirect('entity/'+str(uuid))
		except Exception as e:
			print 'Exception'
			print e
			flash('Form not filled properly')
	else:
		form_error_helper(form)
	return render_template("edit_entity.html", homeclass="active",uuid=str(uuid), entity=entity, form=form)	


##TODO: check if the ending forward slashes are there for all
## do it when checking
@user.route('/temp/')
def temp():
	##fetch current details for now
	##show these current details
	##edit form of entity?
	##wait for moderation	
	return render_template("temp.html", homeclass="active", temptext='temp')

