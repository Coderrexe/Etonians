from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")

    def validate_long_word(self):
        pass
