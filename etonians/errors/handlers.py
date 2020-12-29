from flask import render_template, url_for, Blueprint
from flask_login import current_user

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
    return render_template("errors/403.html", title="Permission denied", image_file=image_file), 403


@errors.app_errorhandler(500)
def error_500(error):
    image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
    return render_template("errors/500.html", title="Server error", image_file=image_file), 500
