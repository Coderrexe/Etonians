import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from etonblog import db, bcrypt
from etonblog.models import User, Post, EmailVerificationCode, TemporaryUser
from etonblog.users.forms import RegistrationForm, VerifyEmailForm, LoginForm, UpdateAccountForm, UpdateAccountPasswordForm, RequestResetForm, ResetPasswordForm
from etonblog.users.utils import save_picture, send_reset_email, send_verify_email

users = Blueprint("users", __name__)


@users.route("/", methods=["GET", "POST"])
@users.route("/register/", methods=["GET", "POST"])
def register():
    # if current user is already logged in, they will be automatically redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = form.email.data
        if "etoncollege.org.uk" not in user_email.split("@", maxsplit=1):
            flash("You must have an Eton College email to register for an account.", "danger")
            return redirect(url_for("users.register"))
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")
        year_group = request.form["year-group"]
        user = TemporaryUser(username=form.username.data, email=form.email.data, password=hashed_password, year_group=year_group)

        db.session.add(user)
        db.session.commit()

        send_verify_email(user.email)

        flash("An email has been sent to you, containing a verification code.", category="info")
        return redirect(url_for("users.verify_email", username=user.username))

    return render_template("register.html", title="Register", form=form)


@users.route("/register/verify/user/<string:username>/", methods=["POST", "GET"])
def verify_email(username):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = VerifyEmailForm()
    if form.validate_on_submit():
        verification_code_list = EmailVerificationCode.query.all()
        for verification_code in verification_code_list:
            if form.verification_code.data == verification_code.value:
                user_info = TemporaryUser.query.filter_by(username=username).first()
                user = User(username=user_info.username, email=user_info.email, password=user_info.password, year_group=user_info.year_group)

                db.session.add(user)         
                db.session.delete(verification_code)       
                db.session.delete(user_info)
                db.session.commit()

                flash("Account successfully created!", category="success")
                login_user(user, remember=True)

                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash("Incorrect verification code.", category="danger")

    return render_template("verify_email.html", title="Verify email", form=form)


@users.route("/login/", methods=["GET", "POST"])
def login():
    # if user is already logged in, they will be redirected back to the home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        # checks if this user is in the database - returns a boolean value
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # compares the hashed password stored in the database with the password the user enters
            login_user(user, remember=True)
            # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        flash("Login Unsuccessful. Please check username and password.", category="danger")

    return render_template("login.html", title="Log In", form=form)


@users.route("/logout/")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("users.login"))
    else:
        return redirect(url_for("users.login"))


@users.route("/account/", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if request.files["profile-picture"]:
            profile_picture = request.files["profile-picture"]
            picture_file = save_picture(profile_picture)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        db.session.commit()
        flash("Your profile has been updated!", category="success")
        return redirect(url_for("users.account"))
    elif request.method == "GET": # if the user simply loaded the page
        form.username.data = current_user.username

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    
    return render_template("account.html", title="Your Account", image_file=image_file, form=form)


@users.route("/account/update_password/", methods=["POST", "GET"])
@login_required
def update_password():
    form = UpdateAccountPasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode("UTF-8")
            current_user.password = hashed_password
            db.session.commit()
            flash("Your password has successfully been updated!", category="success")
            return redirect(url_for("users.account"))
        else:
            flash("Your old password is incorrect.", category="danger")
    
    return render_template("update_password.html", title="Update Password", form=form)


@users.route("/user/<string:username>/")
def user_page(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # filters posts by username and orders them by date posted
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("user_page.html", posts=posts, user=user, image_file=image_file)


@users.route("/reset_password/", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        send_reset_email(current_user)
        flash("An email has been sent to you, with instructions to reset your password.", category="info")
        return redirect(url_for("main.home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # finds the user with the email
        send_reset_email(user)
        flash("An email has been sent to you, with instructions to reset your password.", category="info")
        return redirect(url_for("users.login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>/", methods=["POST", "GET"])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token.", category="warning")
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # it is unsafe to store the user password as plain text
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated!", category="success")
        login_user(user)

        # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home")) # otherwise the user will just be redirected to the home page

    return render_template("reset_token.html", title="Reset Password", form=form)
