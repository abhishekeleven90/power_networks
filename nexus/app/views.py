from app import app
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from functools import wraps
from forms import RegisterationForm, LoginForm
from dbwork import *


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session: 
            flash('Please login first to use this')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
    
@app.route('/')
@app.route('/home/')
def home():
    return render_template("home.html", homeclass="active")


@app.route('/login/')
def login():
    flash("Login here")
    session['userid']='653674'
    #form = form is mandatory here 
    return render_template("login.html", loginclass="active", signincss=True)

#get to land first on signup page, post to actually sign up
@app.route('/signup/', methods=["GET","POST"]) 
def signup():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash('Login details valid')
        return redirect('home')
    #form = form is mandatory here
    return render_template("signup.html", signupclass="active", signincss=True, form=form) 

@app.errorhandler(404)
@app.errorhandler(403)
def page_not_found(e):
    return render_template("error.html", homeclass="active", errortext="Sorry, the page does not exist or you are not permitted to see this.")

@app.route('/temp/')
@login_required
@role_required('admin')
def temp():
    nayaperson = Person.create(name='nayaperson')
    naya_kitty = Pet.create(ownerid=nayaperson, type='cat')
    toflash = ''
    for person in Person.select():
        toflash = toflash + (str(person.id)+" "+person.name) + "\n\r"
    flash(toflash)
    return render_template("temp.html", homeclass="active", temptext=str(nayaperson.id)+" "
        +str(naya_kitty.id))


def get_current_user_role():
    return 'admin'