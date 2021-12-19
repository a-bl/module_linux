from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_add_rater(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.rated.all(), [])
        self.assertEqual(u1.raters.all(), [])

        u1.add_rater(u2)
        db.session.commit()
        self.assertTrue(u1.is_rating(u2))
        self.assertEqual(u1.rated.count(), 1)
        self.assertEqual(u1.rated.first().username, 'susan')
        self.assertEqual(u2.raters.count(), 1)
        self.assertEqual(u2.raters.first().username, 'john')

        u1.remove_rater(u2)
        db.session.commit()
        self.assertFalse(u1.is_rating(u2))
        self.assertEqual(u1.rated.count(), 0)
        self.assertEqual(u2.raters.count(), 0)

    def test_rated_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the raters
        u1.add_rater(u2)  # john rates susan
        u1.add_rater(u4)  # john rates david
        u2.add_rater(u3)  # susan rates mary
        u3.add_rater(u4)  # mary rates david
        db.session.commit()

        # check the rated posts of each user
        f1 = u1.rated_posts().all()
        f2 = u2.rated_posts().all()
        f3 = u3.rated_posts().all()
        f4 = u4.rated_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)