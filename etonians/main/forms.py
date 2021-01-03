from wtforms import StringField

from flask_wtf import FlaskForm

class SearchForm(FlaskForm):
    q = StringField()
