"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return render_template("user-info.html", user=user)

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