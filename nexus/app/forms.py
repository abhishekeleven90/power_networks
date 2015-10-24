from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class RegisterationForm(Form):
    emailid = EmailField('emailid', validators=[validators.DataRequired(), validators.Email()])
    name = StringField('name', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(), 
        validators.EqualTo('repassword',message="Passwords must match")])
    repassword = PasswordField('repassword', validators=[validators.Required()])
    accept_terms = BooleanField('I accept everything!')

class LoginForm(Form):
    emailid = StringField('emailid', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(), 
        validators.EqualTo('confirm',message="Passwords must match")])
    rem_me = BooleanField('Remember me')