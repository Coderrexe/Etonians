from flask import render_template, url_for, flash, redirect, request, Blueprint, g
from flask_login import login_user, current_user, logout_user, login_required

from etonians import db, bcrypt
from etonians.models import User, Post, EmailVerificationCode, TemporaryUser
from etonians.users.forms import RegistrationForm, VerifyEmailForm, LoginForm, UpdateAccountForm, UpdateAccountPasswordForm, RequestResetForm, ResetPasswordForm
from etonians.users.utils import save_picture, send_reset_email, send_verify_email
from etonians.main.forms import SearchForm

users = Blueprint("users", __name__)


@users.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
        g.search_form = SearchForm()


@users.route("/")
@users.route("/authentication/")
def user_authentication():
    # if current user is already logged in, they will be automatically redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    signup_form = RegistrationForm()
    login_form = LoginForm()

    return render_template(
        "login_signup.html",
        signup_form=signup_form,
        login_form=login_form
    )


@users.route("/90bf30f4f67787b8400f597c3406066d/", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "GET":
        return redirect(url_for("users.user_authentication"))
        
    signup_form = RegistrationForm()
    login_form = LoginForm()

    if signup_form.validate_on_submit():
        user_email = signup_form.email.data
        if "etoncollege.org.uk" not in user_email.split("@", maxsplit=1):
            flash("You must have an Eton College email to register for an account.", "danger")
            return redirect(url_for("users.register"))
        
        hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode("UTF-8")
        year_group = request.form["year-group"]
        user = TemporaryUser(username=signup_form.username.data, email=signup_form.email.data, password=hashed_password, year_group=year_group)

        db.session.add(user)
        db.session.commit()

        send_verify_email(user.email)

        flash("An email has been sent to you, containing a verification code.", category="info")
        return redirect(url_for("users.verify_email", username=user.username))
    
    return render_template(
        "login_signup.html",
        signup_form=signup_form,
        login_form=login_form
    )


@users.route("/6db120f1af1291b61dcfc3cc63fbab05/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "GET":
        return redirect(url_for("users.user_authentication"))

    signup_form = RegistrationForm()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # checks if this user is in the database - returns a boolean value
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data): # compares the hashed password stored in the database with the password the user enters
            login_user(user, remember=True)
            # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
            next_page = request.args.get("next")
            flash("You have successfully logged in!", category="success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Please check your username and password.", category="danger")
            return render_template("login_signup.html", signup_form=signup_form, login_form=login_form, is_login_page="true")
    
    return render_template(
        "login_signup.html",
        signup_form=signup_form,
        login_form=login_form
    )


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

    return render_template(
        "verify_email.html",
        title="Verify email",
        form=form
    )


@users.route("/logout/")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have logged out.", category="danger")
        return redirect(url_for("users.user_authentication"))
    else:
        flash("You need to log in first.", "warning")
        return redirect(url_for("users.user_authentication"))


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
    
    return render_template(
        "account.html",
        title="Your Account",
        form=form
    )


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
    
    return render_template(
        "update_password.html",
        title="Update Password",
        form=form
    )


@users.route("/user/<string:username>/")
def user_page(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # filters posts by username and orders them by date posted
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)

    return render_template(
        "user_page.html",
        posts=posts,
        user=user,
    )


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

    return render_template(
        "reset_request.html", 
        title="Reset Password", 
        form=form
    )


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

    return render_template(
        "reset_token.html",
        title="Reset Password",
        form=form
    )
