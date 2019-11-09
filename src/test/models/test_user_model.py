import unittest
from src.model.user_model import UserModel
from src.app import create_app, db


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'user',
            'email': 'user@mail.com',
            'password': 'passw0rd!'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_create(self):
        u = UserModel(self.user)
        self.assertIsNotNone(u)

    def test_user_retrieve(self):
        u = UserModel(self.user)
        db.session.add(u)
        db.session.commit()
        s = UserModel.query.first()
        self.assertEqual(s, u)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
