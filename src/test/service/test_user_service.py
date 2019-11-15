import json
import unittest
from unittest.mock import patch

from src.app import create_app, db
from src.model.user_model import UserModel, UserSchema
from src.service.user_service import UserService

user_schema = UserSchema()


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user1 = {
            'name': 'user',
            'email': 'user@mail.com',
            'password': 'passw0rd!'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_create(self):
        res = UserService.create(user_schema.load(self.user1))

        self.assertEqual(res.status_code, 201)

    def test_user_create_user_with_same_mail(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()

        res = UserService.create(user_schema.load(self.user1))

        self.assertEqual(res.status_code, 400)

    @patch.object(UserService, 'get_user', lambda: 1)
    def test_user_update(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()

        res = UserService.update(user_schema.load({'name': 'test'}, partial=True))

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'test')

    @patch.object(UserService, 'get_user', lambda: 1)
    def test_delete_user(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()

        res = UserService.delete()
        self.assertEqual(res.status_code, 204)

    def test_login(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()
        partial_user = {'email': 'user@mail.com', 'password': 'passw0rd!'}
        res = UserService.login(user_schema.load(partial_user, partial=True))
        self.assertEqual(res.status_code, 200)

    def test_login_no_email_or_password(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()

        res = UserService.login(user_schema.load({'email': 'usdasder@mail.com'}, partial=True))
        self.assertEqual(res.status_code, 400)

        res = UserService.login(user_schema.load({'password': 'passw0rd!'}, partial=True))
        self.assertEqual(res.status_code, 400)

    def test_login_wrong_email(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()
        wrong_email = {'email': 'usdasder@mail.com', 'password': 'passw0rd!'}
        res = UserService.login(user_schema.load(wrong_email, partial=True))
        self.assertEqual(res.status_code, 400)

    def test_login_wrong_password(self):
        user = UserModel(user_schema.load(self.user1))
        user.save()
        wrong_password = {'email': 'user@mail.com', 'password': 'pasdsadasdsssw0rd!'}
        res = UserService.login(user_schema.load(wrong_password, partial=True))
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
