import secrets # secrets module is used to generate random hexes for user profile picture file
import os
from PIL import Image # PIL (Python Imaging Library) resizes user profile picture to make website run faster
from flask import render_template, url_for, flash, redirect, request, abort
from etonblog import app, db, bcrypt, mail
from etonblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from etonblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/home")
@app.route("/home/")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    # displays the latest posts first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4) # accessing all posts in the database - displays 4 posts per page
    # the location of the user's profile picture - stored in etonblog/static/profile_pictures/
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("home.html", posts=posts, image_file=image_file)


@app.route("/about")
@app.route("/about/")
def about():
    if current_user.is_authenticated:
        image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    else:
        image_file = None # if current user is not logged in, there will be no profile picture displayed

    return render_template("about.html", title="About", image_file=image_file)


@app.route("/register", methods=["GET", "POST"])
@app.route("/register/", methods=["GET", "POST"])
def register():
    # if current user is already logged in, they will be automatically redirected to home page
    if current_user.is_authenticated:
        return redirect(url_for("home"))

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
        return redirect(next_page) if next_page else redirect(url_for("home")) # otherwise the user will just be redirected to the home page

    return render_template("register.html", title="Register", form=form)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    # if user is already logged in, they will be redirected back to the home page
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        # checks if this user is in the database - returns a boolean value
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # compares the hashed password stored in the database with the password the user enters
            login_user(user, remember=form.remember.data)
            # if the user wanted to access a page that was @loginrequired before logging in, they will be redirected to that page
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/donate")
@app.route("/donate/")
def donate():
    if current_user.is_authenticated:
        image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    else:
        image_file = None

    return render_template("donate.html", title="Donate", image_file=image_file)


@app.route("/logout")
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_picture(form_picture):
    # picture files will be turned into random_hexes in order to prevent pictures of the same name
    random_hex = secrets.token_hex(8) 
    _, file_extension = os.path.splitext(form_picture.filename) # "_" is used for throwaway variables
    picture_file_name = random_hex + file_extension
    # stores the picture to the profile_pictures folder
    picture_path = os.path.join(app.root_path, "static/profile_pictures/", picture_file_name)

    # resize the profile picture to 200 pixels by 200 pixels
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_file_name


@app.route("/account", methods=["POST", "GET"])
@app.route("/account/", methods=["POST", "GET"])
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
        return redirect(url_for("account"))
    elif request.method == "GET": # if the user simply loaded the page
        form.username.data = current_user.username # The boxes should already filled with the current user data
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("account.html", image_file=image_file, form=form)


@app.route("/post/new", methods=["POST", "GET"])
@app.route("/post/new/", methods=["POST", "GET"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("New post successfully created!", "success")
        return redirect(url_for("home"))

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("create_post.html", title="New Post", form=form, image_file=image_file)


@app.route("/post/<int:post_id>")
@app.route("/post/<int:post_id>/")
@login_required
def post(post_id): # the posts are sorted by ID
    post = Post.query.get_or_404(post_id)
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("post.html", title=post.title, post=post, image_file=image_file)


@app.route("/post/<int:post_id>/update", methods=["POST", "GET"])
@app.route("/post/<int:post_id>/update/", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    if post.author != current_user: # if a user is trying to update someone else's post, then 403 error
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data # updates the old post title and content with new title and content
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been successfully updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET": # if the user simply loads the page
        form.title.data = post.title # the boxes are already filled in with the non-updated post title and content
        form.content.data = post.content

    return render_template("update_post.html", title="Update Post", form=form, image_file=image_file)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@app.route("/post/<int:post_id>/delete/", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author: # if the user tries to delete someone else's post, then 403 error
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))


# every registered user have their own page, which displays information about them and all of their posts
@app.route("/user/<string:username>")
@app.route("/user/<string:username>/")
def user_page(username):
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # filters posts by username and orders them by date posted
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_page.html", posts=posts, user=user, image_file=image_file)


# this function is called in reset_request route, and sends an email to the user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@etonians.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for("reset_token", token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


@app.route("/reset_password", methods=["POST", "GET"])
@app.route("/reset_password/", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # finds the user with the email
        send_reset_email(user)
        flash("An email has been sent to your email, with instructions to reset your password.", "info")
        return redirect(url_for("login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["POST", "GET"])
@app.route("/reset_password/<token>/", methods=["POST", "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))

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
        return redirect(next_page) if next_page else redirect(url_for("home")) # otherwise the user will just be redirected to the home page

    return render_template("reset_token.html", title="Reset Password", form=form)
