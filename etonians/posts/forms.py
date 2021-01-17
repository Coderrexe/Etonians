from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from flask_wtf import FlaskForm


class PostForm(FlaskForm):
    title = StringField(
        label="Title",
        validators=[DataRequired(), Length(max=150, message="Title is longer than 150 characters")]
    )
    content = TextAreaField(label="Content", validators=[DataRequired()])
    submit = SubmitField(label="Post")

    def validate_long_word(self):
        # this function will be written in future commits
        pass
