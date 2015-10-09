from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms import validators

class RegisterationForm(Form):
    email = StringField('openid', validators=[validators.DataRequired()])
    name = StringField('openid', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(), 
        validators.EqualTo('confirm',message="Passwords must match")])
    repassword = PasswordField('repassword', validators=[validators.Required()])
    accept_tems = BooleanField('I accept everything!')

class LoginForm(Form):
    userid = StringField('userid', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(), 
        validators.EqualTo('confirm',message="Passwords must match")])
    rem_me = BooleanField('Remember me')