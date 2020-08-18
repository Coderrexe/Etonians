from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField # EmailField makes it easier to enter an email address on mobile
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from etonblog.models import User


# registration form and login form
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20, message="Must be between 2 and 20 characters long.")])
    email = EmailField("Email", validators=[DataRequired(), Email(message="Email is not valid.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign Up")

    # validate_username and validate_email functions will be automatically called
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already used by another account. Please choose another one.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email is already associated with another account.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message="Email is not valid.")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"])])
    submit = SubmitField("Update")

    # validate_username and validate_email functions will be automatically called
    def validate_username(self, username):
        if username.data != current_user.username: # function will be only carried out if the user decides to actually change its username
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is already used by another account. Please choose another one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("This email is already associated with another account.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message="Email is not valid.")])
    submit = SubmitField("Reset Password")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError("No user found.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Reset Password")
