from flask import render_template, url_for, request, Blueprint
from flask_login import current_user, login_required
from etonblog.models import Post

main = Blueprint("main", __name__)


@main.route("/home")
@main.route("/home/")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    filter_year_group = request.args.get("filter_year_group", "All", type=str)

    if filter_year_group == "All":
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).filter_by(year_group=filter_year_group).paginate(page=page, per_page=1)

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("home.html", posts=posts, image_file=image_file)


@main.route("/about")
@main.route("/about/")
def about():
    if current_user.is_authenticated:
        image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    else:
        image_file = None # if current user is not logged in, there will be no profile picture displayed

    return render_template("about.html", title="About", image_file=image_file)


@main.route("/donate")
@main.route("/donate/")
def donate():
    if current_user.is_authenticated:
        image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    else:
        image_file = None

    return render_template("donate.html", title="Donate", image_file=image_file)
