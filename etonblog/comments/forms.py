from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length


class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[Length(min=5, max=200)])
    submit = SubmitField("Comment")
