"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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