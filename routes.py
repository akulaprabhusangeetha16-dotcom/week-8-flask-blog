from flask import render_template, redirect, url_for, request
from app import db
from app.models import Post
from app.posts import posts_bp

@posts_bp.route("/")
def home():

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("main/home.html", posts=posts)


@posts_bp.route("/post/create", methods=["GET","POST"])
def create_post():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        post = Post(title=title, content=content)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("posts.home"))

    return render_template("posts/create.html")


@posts_bp.route("/post/<int:id>")
def view_post(id):

    post = Post.query.get_or_404(id)

    return render_template("posts/detail.html", post=post)


@posts_bp.route("/post/edit/<int:id>", methods=["GET","POST"])
def edit_post(id):

    post = Post.query.get_or_404(id)

    if request.method == "POST":

        post.title = request.form["title"]
        post.content = request.form["content"]

        db.session.commit()

        return redirect(url_for("posts.home"))

    return render_template("posts/edit.html", post=post)


@posts_bp.route("/post/delete/<int:id>")
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("posts.home"))