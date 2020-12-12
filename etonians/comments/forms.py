from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    title = StringField(label="Title (optional)", validators=[Length(max=100)])
    content = TextAreaField(label="Content", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField(label="Reply")
