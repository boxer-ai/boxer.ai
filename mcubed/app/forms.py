from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SiteForm(Form):
    url = StringField('url', validators=[DataRequired()])
    descr = BooleanField('descr', default=False)
