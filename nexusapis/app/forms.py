from flask.ext.wtf import Form, widgets
from flask import flash, request
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SelectMultipleField, widgets, RadioField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms import DateTimeField, Field
from wtforms.widgets import TextInput

class ListField(Field):

    widget = TextInput()

    def _value(self):
        if self.data:
            import ast
            return ast.literal_eval(self.data)
            return
        else:
            return []

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = str(valuelist)
        else:
            self.data = []


class RegisterationForm(Form):
    emailid = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    name = StringField('name', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.Required(),
        validators.EqualTo('repassword',message="Passwords must match")])
    repassword = PasswordField('repassword', validators=[validators.Required()])
    accept_terms = BooleanField('I accept everything!')

class AddRelationForm(Form):
    startnodeid = IntegerField('From UUID', validators=[validators.DataRequired()])
    endnodeid = IntegerField('To UUID', validators=[validators.DataRequired()])
    reltype = StringField('Relation Type', validators=[validators.DataRequired()])

class LoginForm(Form):
    emailid = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.Required()])
    ##rem_me = BooleanField('Remember me')
    ##TODO: some time afterwards

class URLForm(Form):
    url = StringField('URL',validators=[validators.DataRequired(),validators.URL('Not a valid URL')])

class EditEntityForm(Form):
    new_entity = TextAreaField('new_entity', validators=[validators.Required()])

# class MergeNodeForm(Form):
#     mult = [('1', 'Choice1'), ('2', 'Choice2'), ('3', 'Choice3')]
#     mult = SelectMultipleField(choices = mult, default = ['1', '3']) ##No validators for now!
#     pass

def form_error_helper(form):
    for field, errors in form.errors.items():
           for error in errors:
               flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))

## AFTER SLUMBER CODE!

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=True)
    option_widget = widgets.CheckboxInput()


# class EntityValidForm(Form):
#     id = IntegerField('Internal ID',validators=[validators.DataRequired()])
#     ##also write a validator here that the id should be unique in all the ids
#     ##also write a validator here that the id is not in neo4j core
#     fetchdate = IntegerField('Fetch date',validators=[validators.DataRequired()])
#     sourceurl = StringField('URL',validators=[validators.DataRequired(),validators.URL('Not a valid URL')])
#     labels  = ListField('Labels',validators=[validators.DataRequired()])
#     print labels.data
#     print type(labels.data)
