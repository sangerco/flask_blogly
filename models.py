"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Users """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String)

    def __repr__(self):
        u = self
        return f"<User: {u.first_name} {u.last_name}>"

    def get_full_name(self):
        """ return the full name of the user as a single string """
        u = self

        if u.middle_name:
            return f"{u.first_name} {u.middle_name} {u.last_name}"
        else:
            return f"{u.first_name} {u.last_name}"

class Post(db.Model):
    """ model for blog post table """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # creates relationship between User and Post models
    user = db.relationship("User", backref='posts')

    @property
    def formatted_date(self):
        return self.created_at.strftime("%a %b %d %Y, %I:%M %p")

class Tag(db.Model):
    """ model for tag table """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):
    """ model for posts_tags table """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        nullable=False,
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                        db.ForeignKey('tags.id'), 
                        nullable=False,
                        primary_key=True)

    tags = db.relationship('Tag', backref='posts_tags')

def connect_db(app):
    """  Connect database to app """

    db.app = app
    db.init_app(app)