from flask import render_template, url_for, redirect, request, flash, abort, Blueprint
from flask_login import current_user, login_required

from etonians import db
from etonians.models import Comment
from etonians.comments.forms import CommentForm

comments = Blueprint("comments", __name__)


@comments.route("/comment/id/<int:comment_id>/edit/", methods=["POST", "GET"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.author:
        abort(403)
    
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

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    
    return render_template("edit_comment.html", title=comment.title, form=form, image_file=image_file)


@comments.route("/comment/id/<int:comment_id>/delete/", methods=["POST", "GET"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id

    if current_user != comment.author:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for("posts.post", post_id=post_id))
