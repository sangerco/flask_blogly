"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "doggo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home_page():
    """ redirect to user list page """
    return redirect ('/users')

@app.route("/users")
def user_listing():
    """ shows list of users """
    users = User.query.order_by(User.last_name)
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user():
    """ show form to add new users """
    return render_template('add-user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """ take new user info and post to database """
    first_name = request.form["first_name"]
    middle_name = request.form["middle_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, middle_name=middle_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ show details for user """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("user-info.html", user=user, posts=posts)

@app.route('/users/edit/<int:user_id>')
def show_edit_user_form(user_id):
    """ display user details and provide cancel and save buttons """
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    """ take edited user info and post to database """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()

    return redirect ('/users')

@app.route("/users/delete/<int:user_id>")
def delete_user(user_id):
    """ delete user from database and return to users page """

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect ('/users')

@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """ display form to create new post """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name)
    return render_template("new-post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_new_post(user_id):
    """ add created post to database, return to user profile page """
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    title = request.form["title"]
    content = request.form["content"]
    user_id = user.id

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect ('/users')
    

@app.route("/users/posts/<int:post_id>")
def display_posts(post_id):
    """ show individual post """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name)
    return render_template("post-info.html", post=post, tags=tags)

@app.route('/users/edit/posts/<int:post_id>')
def show_edit_post_form(post_id):
    """ display post details and provide cancel and save buttons """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name)
    return render_template("edit-post.html", post=post, tags=tags)

@app.route('/users/edit/posts/<int:post_id>', methods=['POST'])
def edit_post(post_id):
    """ submit post changes to db and return to user page """
    title = request.form["title"]
    content = request.form["content"]
    
    post = Post.query.get(post_id)
    user_id = post.user_id
    post.title = title
    post.content = content
    post.user_id = user_id

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect ('/users')

@app.route("/users/posts/delete/<int:post_id>")
def delete_post(post_id):
    """ delete user from database and return to users page """

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect ('/users')

@app.route('/tags')
def show_tags():
    """ show list of created tags """
    tags = Tag.query.order_by(Tag.name)
    return render_template("tags.html", tags=tags)

@app.route("/tags/new")
def new_tag():
    """ show form to add new tag to post """
    posts = Post.query.all()
    return render_template("create-tag.html", posts=posts)

@app.route("/tags/new", methods=['POST'])
def create_new_tag():
    """ submit data to create new tag and return to tags page """

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    name = request.form["name"]

    new_tag = Tag(name=name, posts=posts)
    db.session.add(new_tag)
    db.session.commit()

    return redirect ('/tags')

@app.route("/tags/<int:tag_id>")
def tag_page(tag_id):
    """ page showing links to tagged posts, as well as edit and delete buttons """
    tag = Tag.query.get_or_404(tag_id)
    posts = Tag.query.get(tag_id).posts
    return render_template('tag-info.html', tag=tag, posts=posts)

@app.route("/tags/edit/<int:tag_id>")
def edit_tag(tag_id):
    """ show form to edit tag """
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("edit-tag.html", tag=tag, posts=posts)
    

@app.route("/tags/edit/<int:tag_id>", methods=['POST'])
def submit_edit_tag(tag_id):
    """ submit data to create new tag and return to tags page """
    tag = Tag.query.get(tag_id)
    name = request.form["name"]
    
    
    tag.name = name
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect ('/tags')

@app.route("/tags/delete/<int:tag_id>")
def delete_tag(tag_id):
    """ delete user from database and return to users page """

    tag = Post.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect ('/tags')