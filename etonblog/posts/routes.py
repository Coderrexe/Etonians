from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from etonblog import db
from etonblog.models import Post, Comment
from etonblog.posts.forms import PostForm
from etonblog.comments.forms import CommentForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["POST", "GET"])
@posts.route("/post/new/", methods=["POST", "GET"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        filter_year_group_list = request.form.getlist("filter_year_group")
        filter_year_group = ""
        
        if filter_year_group_list:
            for year_group in filter_year_group_list:
                filter_year_group += year_group
            post = Post(title=form.title.data, content=form.content.data, author=current_user, year_group=current_user.year_group, filter_year_group=filter_year_group)
            db.session.add(post)
            db.session.commit()
            flash("New post successfully created!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Tick at least one of the year group boxes to proceed.", "danger")

    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("create_post.html", title="New Post", form=form, image_file=image_file)


@posts.route("/post/id/<int:post_id>", methods=["POST", "GET"])
@posts.route("/post/id/<int:post_id>/", methods=["POST", "GET"])
@login_required
def post(post_id): # every post has a unique ID
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post=post)
    if form.validate_on_submit():
        comment = Comment(title=form.title.data, content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("posts.post", post_id=post_id))
    
    image_file = url_for("static", filename=f"profile_pictures/{current_user.image_file}")
    return render_template("post.html", title=post.title, form=form, post=post, comments=comments, image_file=image_file)


@posts.route("/post/id/<int:post_id>/edit", methods=["POST", "GET"])
@posts.route("/post/id/<int:post_id>/edit/", methods=["POST", "GET"])
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
        return redirect(url_for("main.home"))
    elif request.method == "GET": # if the user simply loads the page
        form.title.data = post.title # the boxes are already filled in with the non-updated post title and content
        form.content.data = post.content

    return render_template("update_post.html", title="Update Post", form=form, image_file=image_file)


@posts.route("/post/id/<int:post_id>/delete", methods=["POST", "GET"])
@posts.route("/post/id/<int:post_id>/delete/", methods=["POST", "GET"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author: # if the user tries to delete someone else's post, then 403 error
        abort(403)
    for comment in Comment.query.filter_by(post_id=post.id):
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("main.home"))
