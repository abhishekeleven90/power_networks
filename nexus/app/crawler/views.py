from app.crawler import crawler
from flask import render_template, flash, redirect, session, request, url_for, current_app
from app.models.dbmodels.tasks import Tasks, Tasklog, Taskusers


@crawler.route('/')
def crawler_home():

    ##TODO - set up variables and render user homepage
    return

##Show add task page
@crawler.route('/addtask/', methods=['GET', 'POST'])
def addtask():
    return render_template('new_task.html', homeclass="active")


@crawler.route('/submittask/', methods=['POST'])
def newtask():

    ##TODO -  create a new task element in db
    owner = request.form['ownerid']
    description = request.form['desc']
    iscrawled = request.form['iscrawled']
    name = request.form['nametask']

    task = Tasks(ownerid=owner, name=name, description=description, iscrawled=iscrawled)
    task.create()
    taskusers = Taskusers(userid=ownerid, taskid=task.taskid)

    return


