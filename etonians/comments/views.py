from flask import render_template, url_for, redirect, request, flash, Blueprint, g
from flask_login import current_user, login_required

from etonians import db
from etonians.models import Comment
from etonians.comments.forms import CommentForm
from etonians.main.forms import SearchForm

comments = Blueprint("comments", __name__)


@comments.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
        g.search_form = SearchForm()


@comments.route("/comment/id/<int:comment_id>/edit/", methods=["POST", "GET"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if current_user != comment.author:
        flash("You can only edit your own replies!", category="danger")
        return redirect(url_for("main.home"))
    
    form = CommentForm()
    if form.validate_on_submit():
        comment.title = form.title.data
        comment.content = form.content.data
        db.session.commit()
        flash("Your reply has successfully been edited!", category="success")
        return redirect(url_for("posts.post", post_id=comment.post.id))
    elif request.method == "GET":
        form.title.data = comment.title
        form.content.data = comment.content
    
    return render_template(
        "edit_comment.html",
        title=comment.title,
        form=form
    )


@comments.route("/comment/id/<int:comment_id>/delete/", methods=["POST", "GET"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id

    if current_user != comment.author:
        flash("You can only delete your own replies!", category="danger")
        return redirect(url_for("main.home"))

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for("posts.post", post_id=post_id))
