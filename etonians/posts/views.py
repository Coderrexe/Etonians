from datetime import datetime

import elasticsearch

from flask import render_template, url_for, flash, redirect, request, Blueprint, g
from flask_login import current_user, login_required

from etonians import db
from etonians.models import Post, Comment
from etonians.utils import convert_date
from etonians.posts.forms import PostForm
from etonians.comments.forms import CommentForm
from etonians.main.forms import SearchForm

posts = Blueprint("posts", __name__)


@posts.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.image_file = url_for("static", filename=f"user_images/{current_user.image_file}")
        g.search_form = SearchForm()
        g.current_time = datetime.utcnow()


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

            post = Post(
                title=form.title.data,
                content=form.content.data, 
                author=current_user,
                year_group=current_user.year_group,
                filter_year_group=filter_year_group
            )
            
            db.session.add(post)
            db.session.commit()
            flash("New post successfully created!", category="success")
            return redirect(url_for("main.home"))
        else:
            flash("Tick at least one of the year group boxes to proceed.", category="danger")

    return render_template(
        "create_post.html",
        title="New Post",
        form=form
    )


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
        flash("Your reply has successfully been created!", category="success")
        return redirect(url_for("posts.post", post_id=post_id))
    
    return render_template(
        "post.html",
        title=post.title,
        form=form,
        post=post,
        comments=comments,
        convert_date=convert_date
    )


@posts.route("/post/id/<int:post_id>/edit/", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash("You can only edit your own posts!", category="danger")
        return redirect(url_for("main.home"))

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data # updates the old post title and content with new title and content
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been successfully updated!", category="success")
        return redirect(url_for("main.home"))
    elif request.method == "GET": # if the user simply loads the page
        form.title.data = post.title # the boxes are already filled in with the non-updated post title and content
        form.content.data = post.content
    
    return render_template(
        "update_post.html",
        title="Update Post",
        form=form
    )


@posts.route("/post/id/<int:post_id>/delete/", methods=["POST", "GET"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user != post.author: # if the user tries to delete someone else's post, then 403 error
        flash("You can only delete your own posts!", category="danger")
        return redirect(url_for("main.home"))

    for comment in Comment.query.filter_by(post_id=post.id):
        db.session.delete(comment)
        db.session.commit()

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", category="danger")
    
    return redirect(url_for("main.home"))


@posts.route('/search')
def search_posts():
    try:
        query = request.args.get("q")
        if not query:
            return redirect(url_for("main.home"))
            
        g.search_form.q.data = query
        posts, total = Post.search(query)
    except elasticsearch.exceptions.ConnectionError:
        flash("Sorry, the search functionality is currently under maintenance.", category="danger")
        return redirect(url_for("main.home"))

    return render_template(
        "home.html",
        title=f"({total}) {query}",
        posts=posts,
        total=total,
        convert_date=convert_date,
        search_text=query
    )
