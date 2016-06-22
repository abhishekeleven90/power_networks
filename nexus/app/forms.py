from flask.ext.wtf import Form, widgets
from flask import flash, request
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SelectMultipleField, widgets, RadioField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField

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



class MergeNodeForm(Form):
    conf_props = []
    #radiobtn = RadioField('Radio', choices=[('1','description'),('2','whatever')], default = '2')
    labels = MultiCheckboxField('Labels 2 add', choices=[])
    new_props = MultiCheckboxField('NewProps 2 add', choices=[])

    def setLabels(self, labels_list):
        self.labels.choices = [(x, x) for x in labels_list]

    def setNewProps(self, new_props_list):
        self.new_props.choices = [(x, x) for x in new_props_list]

    def setConfProps(self, propList, oldList, newList):
        for i in range(len(propList)):
            prop = propList[i]
            old = oldList[i]
            naya = newList[i]
            radiobtn = RadioField(prop, choices=[(old, old),(naya,naya)], default = old)
            self.conf_props.append(radiobtn)


class MyForm():
    conf_props = []
