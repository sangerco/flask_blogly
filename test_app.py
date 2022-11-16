from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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
        ''' add test post '''

        User.query.delete()

        user = User(first_name="Bob", last_name="Newhart", image_url="https://tinyurl.com/3pb9wkad")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="Title", content="content", user_id=1)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        tag = Tag(name='test_tag')

        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

        post_tag = PostTag(post_id = 1, tag_id = 1)

        db.session.add(post_tag)
        db.session.commit()

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
            self.assertIn('Title', html)
            self.assertIn('<img src="https://tinyurl.com/3pb9wkad" alt="Picture of Bob Newhart" height="300">', html)

    def test_add_user(self):
        """ test to add new user to list """
        with app.test_client() as client:
            user = {"first_name": "Conan", "middle_name": "", "last_name": "OBrien", "image_url": "http://fake_url.com"}
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

    def test_show_new_post_form(self):
        """ test to show new post form """
        with app.test_client() as client:
            res = client.get(f"users/{self.user_id}/posts/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn('<form id="form" action="/users/3/posts/new" method="POST">', html)


    def test_add_post(self):
        """ test to add new post to list """
        with app.test_client() as client:
            post = {"title": "test post", "content": "content", "user_id": 1}
            res = client.post(f"/users/{self.user_id}/posts/new", data = post, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('test post', html)



    def test_view_post(self):
        """ test to view posts """
        with app.test_client() as client:
            res = client.get(f"/users/posts/{self.post_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('test_tag', html)
            self.assertIn('Title', html)

    def test_edit_post(self):
        """ test to edit existing post """
        with app.test_client() as client:
            post = {"title": "Edited", "content": "edited"}
            res = client.post(f"/users/edit/posts/{self.post_id}", data = post, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Edited", html)

    def test_delete_post(self):
        """ test to delete existing post """
        with app.test_client() as client:
            res = client.get(f"/users/posts/delete/{self.post_id}", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("Title", html)

    def test_show_tags(self):
        """ test to show tags """
        with app.test_client() as client:
            res = client.get('/tags')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/tags/1">test_tag</a>', html)


    def test_show_add_tag_form(self):
        """ test to create tag """
        with app.test_client() as client:
            res = client.get("/tags/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<input type="text" class="form-control" name="name">', html)

    def test_add_tag(self):
        """ test to add tag """
        with app.test_client() as client:
            tag = {"name": "tag 2"}
            res = client.post("tags/new", data = tag, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('tag 2', html)

    def test_edit_tag(self):
        """ test to edit existing tag """
        with app.test_client() as client:
            tag = {"name": "Edited"}
            res = client.post(f"/tags/edit/{self.tag_id}", data = tag, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Edited", html)

    def test_delete_post(self):
        """ test to delete tags """
        with app.test_client() as client:
            res = client.get(f"/tags/delete/{self.tag_id}", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("test_tag", html)