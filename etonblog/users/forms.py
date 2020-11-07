from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from etonblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(label="Nickname", validators=[DataRequired(), Length(min=2, max=20, message="Must be between 2 and 20 characters long.")])
    email = EmailField(label="Email", validators=[DataRequired(), Email(message="Email is not valid.")])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign Up")

    # validate_username and validate_email functions will be automatically called
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(message="This username is already used by another account. Please choose another one.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(message="This email is already associated with another account.")


class VerifyEmailForm(FlaskForm):
    verification_code = IntegerField(label="Verification Code", validators=[DataRequired()])
    submit_button = SubmitField(label="Register Account")


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Log In")


class UpdateAccountForm(FlaskForm):
    username = StringField(label="Change Username", validators=[DataRequired(), Length(min=2, max=20)])
    submit_button = SubmitField(label="Update")

    # validate_username and validate_email functions will be automatically called
    def validate_username(self, username):
        if username.data != current_user.username: # function will be only carried out if the user decides to actually change its username
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(message="This username is already used by another account. Please choose another one.")


class UpdateAccountPasswordForm(FlaskForm):
    old_password = PasswordField(label="Your Old Password", validators=[DataRequired()])
    new_password = PasswordField(label="Your New Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    confirm_new_password = PasswordField(label="Confirm New Password", validators=[DataRequired(), EqualTo("new_password", message="Passwords must match.")])
    submit_button = SubmitField(label="Change Password")


class RequestResetForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email(message="Email is not valid.")])
    submit = SubmitField(label="Reset Password")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError(message="This email is not registered with any accounts on Etonians.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, message="Must be at least 8 characters long.")])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField(label="Reset Password")
