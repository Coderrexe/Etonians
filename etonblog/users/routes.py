from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from etonblog import db, bcrypt
from etonblog.models import User, Post
from etonblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from etonblog.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
@users.route("/register/", methods=["GET", "POST"])
def register():
    # if current user is already logged in, they will be automatically redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # it is unsafe to store the user password as plain text
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created! You can now login.", "success")
        login_user(user, remember=form.remember.data)
        # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home")) # otherwise the user will just be redirected to the home page

    return render_template("register.html", title="Register", form=form)


@users.route("/", methods=["GET", "POST"])
@users.route("/login", methods=["GET", "POST"])
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
            login_user(user, remember=form.remember.data)
            # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check username and password.", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@users.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["POST", "GET"])
@users.route("/account/", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: # profile picture is not a required field (users can just use the default picture)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file # updates the profile picture
        # updates different fields
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET": # if the user simply loaded the page
        form.username.data = current_user.username # The boxes should already filled with the current user data
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("account.html", image_file=image_file, form=form)


# every registered user have their own page, which displays information about them and all of their posts
@users.route("/user/<string:username>")
@users.route("/user/<string:username>/")
def user_page(username):
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # filters posts by username and orders them by date posted
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_page.html", posts=posts, user=user, image_file=image_file)


@users.route("/reset_password", methods=["POST", "GET"])
@users.route("/reset_password/", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # finds the user with the email
        send_reset_email(user)
        flash("An email has been sent to your email, with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["POST", "GET"])
@users.route("/reset_password/<token>/", methods=["POST", "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # it is unsafe to store the user password as plain text
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated!", "success")
        login_user(user)
        # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.home")) # otherwise the user will just be redirected to the home page

    return render_template("reset_token.html", title="Reset Password", form=form)
