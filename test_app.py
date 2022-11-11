from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class TestUserClass(TestCase):
    ''' Testing for creating and viewing test users '''

    def setUp(self):
        ''' add test user '''

        User.query.delete()

        user = User(first_name="Bob", last_name="Newhart", image_url="https://tinyurl.com/3pb9wkad")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        ''' clear out session for next test '''

        db.session.rollback()

    def test_get_users(self):
        """ test to get existing list of users """
        with app.test_client() as client:
            res = client.get("/", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Bob Newhart", html)

    def test_view_user(self):
        """ test to view existing user info """
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<img src="https://tinyurl.com/3pb9wkad" alt="Picture of Bob Newhart" width="300">', html)

    def test_add_user(self):
        """ test to add new user to list """
        with app.test_client() as client:
            user = {"first_name": "Conan", "last_name": "OBrien", "image_url": "http://fake_url.com"}
            res = client.post("/users/new", data = user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Conan OBrien", html)

    def test_edit_user(self):
        """ test to edit existing user """
        with app.test_client() as client:
            user = {"first_name": "Bud", "last_name": "Newhart", "image_url": "http://fake_url.com"}
            res = client.post(f"/users/edit/{self.user_id}", data = user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Bud Newhart", html)

    def test_delete_user(self):
        """ test to delete existing user """
        with app.test_client() as client:
            res = client.get(f"/users/delete/{self.user_id}", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("Bob Newhart", html)



