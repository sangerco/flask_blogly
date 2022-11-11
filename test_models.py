from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class TestUserModel(TestCase):
    """ test user method """

    def setUp(self):
        """ clear out any data left in session """

        User.query.delete()

    def tearDown(self):
        """ empty session for next test """

        db.session.rollback()

    def test_full_name_method(self):
        """ test for full name method """

        user = User(first_name="Bob", last_name="Newhart", image_url="http://fake_url.com")
        self.assertEquals(user.get_full_name(), "Bob Newhart")

    def test_full_name_method_with_middle_name(self):
        """ test for full name method with middle name """

        user = User(first_name="Joe", middle_name="Don", last_name="Baker", image_url="http://fake_url.com")
        self.assertEquals(user.get_full_name(), "Joe Don Baker")
