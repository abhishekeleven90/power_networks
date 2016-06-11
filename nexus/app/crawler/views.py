from app.crawler import crawler
from flask import render_template, flash, redirect, session, request, url_for, abort
from app.models.dbmodels.tasks import Tasks, Tasklog, Taskusers
from app.forms import EditEntityForm, form_error_helper


##Show add task page
@crawler.route('/addtask/', methods=['GET', 'POST'])
def addtask():
    userid = 'abhi7@gmail.com'
    key = 'some-random-key'
    return render_template('new_task.html', homeclass="active",
                           userid=userid, api_key=key)


@crawler.route('/submittask/', methods=['POST'])
def submittask():

    owner = request.form['ownerid']
    description = request.form['desc']
    name = request.form['nametask']

    try:
        task = Tasks(ownerid=owner, name=name, description=description)
        task.create()
        taskusers = Taskusers(userid=owner, taskid=task.taskid)
        taskusers.create()
    except Exception as e:
        flash('Task creation error')
        print e.message
    else:
        flash('Task successfully created')
    return redirect(url_for('.crawler_home'))


@crawler.route('/')
def crawler_home():
    ## TODO - show user dashboard
    return render_template("crawler_home.html", temptext='crawler')


@crawler.route('/listtasks/')
def listtasks():
    ##TODO - list all tasks given a user id
    userid = session.get('userid')
    tasks_of_user = Taskusers(userid=userid)
    taskids = tasks_of_user.getListFromDB('userid')
    taskobjlist = []
    for i in taskids:
        taskobj = Tasks.getTask(i)
        tmptaskusr = Taskusers(taskid=i)
        users_list = tmptaskusr.getListFromDB('taskid')
        n_users = len(users_list)
        tmpdict = {"name": taskobj.name, "ownerid": taskobj.ownerid,
                   "taskid": i, "users": n_users}
        taskobjlist.append(tmpdict.copy())

    return render_template("list_tasks.html", temptext='list the tasks here',
                           usr_list=taskobjlist)


## TODO - use taskid as route parameter
@crawler.route('/showtask/<int:taskid>')
def showtask(taskid):
    ##TODO - show a particular task and its recent activities
    userid = session.get('userid')
    task = Tasks.getTask(taskid)
    data = task.__dict__.copy()
    tasklog = Tasklog(taskid=taskid)
    logobjs = tasklog.getListFromDB(taskid)
    return render_template("show_task.html", task=data, logs=logobjs)
