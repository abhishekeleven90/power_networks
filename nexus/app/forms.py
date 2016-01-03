from flask.ext.wtf import Form
from flask import flash
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class RegisterationForm(Form):
    emailid = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    name = StringField('name', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(), 
        validators.EqualTo('repassword',message="Passwords must match")])
    repassword = PasswordField('repassword', validators=[validators.Required()])
    accept_terms = BooleanField('I accept everything!')

class LoginForm(Form):
    emailid = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.Required()])
    ##rem_me = BooleanField('Remember me')
    ##TODO: some time afterwards

class EditEntityForm(Form):
    new_entity = TextAreaField('new_entity', validators=[validators.Required()])

def form_error_helper(form):
    for field, errors in form.errors.items():
           for error in errors:
               flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))

