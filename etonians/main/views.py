from datetime import datetime

from flask import render_template, url_for, redirect, Blueprint, g, current_app
from flask_login import current_user, login_required

from etonians.models import Post
from etonians.utils import convert_date
from etonians.main.forms import SearchForm

main = Blueprint("main", __name__)


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
        g.search_form = SearchForm()
        g.current_time = datetime.utcnow()


@main.route("/")
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    else:
        return redirect(url_for("users.user_authentication"))


@main.route("/home/")
@login_required
def home():
    posts = []

    for post in Post.query.all():
        if current_user.year_group in post.filter_year_group:
            posts.append(post)

    posts = posts[::-1]
    
    return render_template(
        "home.html",
        title="Home",
        posts=posts,
        convert_date=convert_date
    )


@main.route("/sw.js")
def service_worker():
    return current_app.send_static_file("js/sw.js")


@main.route("/no-internet")
def offline():
    return current_app.send_static_file("offline.html")


@main.route("/about/")
def about():
    if current_user.is_authenticated:
        image_file = g.image_file
    else:
        image_file = None

    return render_template(
        "about.html",
        title="About",
        image_file=image_file
    )
