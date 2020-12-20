from datetime import datetime
from flask import render_template, url_for, Blueprint
from flask_login import current_user, login_required

from etonians.models import Post
from etonians.utils import convert_date

main = Blueprint("main", __name__)


@main.route("/home/")
@login_required
def home():
    posts = []

    for post in Post.query.all():
        if current_user.year_group in post.filter_year_group:
            posts.append(post)

    posts = posts[::-1]
    
    current_time = datetime.utcnow()
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")

    return render_template("home.html", title="Home", posts=posts, image_file=image_file, current_time=current_time, convert_date=convert_date)


@main.route("/about/")
def about():
    if current_user.is_authenticated:
        image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    else:
        image_file = None

    return render_template("about.html", title="About", image_file=image_file)
