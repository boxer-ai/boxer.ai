from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class SiteForm(Form):
    siteinput = StringField('url', validators=[DataRequired()])
    descr = BooleanField('descr', default = False)
