import unittest
import json
from src.app import create_app, db


class UsersTest(unittest.TestCase):

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

    """
    Helper Methods
    """

    def test_user_registration(self):
        """ test user registration with valid credentials """
        res = self.register(self.user)
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    def register(self, user):
        return self.client().post('/api/users/register', headers={'Content-Type': 'application/json'},
                                  data=json.dumps(user))

    """
    Test Methods
    """

    def test_user_registration_with_existing_email(self):
        """ test user registration with already existing email"""
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        res = self.register(self.user)
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_user_registration_with_no_password(self):
        """ test user registration with no password"""
        user1 = {
            'name': 'user',
            'email': 'user1@mail.com',
        }
        res = self.register(user1)
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('schema_errors'))

    def test_user_registration_with_no_email(self):
        """ test user registration with no email """
        user1 = {
            'name': 'user',
            'pasword': 'user1@mail.com',
        }
        res = self.register(user1)
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('schema_errors'))

    def test_user_registration_with_empty_request(self):
        """ test user registration with empty request """
        user1 = {}
        res = self.register(user1)
        self.assertEqual(res.status_code, 400)

    def test_user_login(self):
        """ User Login Tests """
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    def test_user_login_with_invalid_password(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'user',
            'email': 'user@mail.com',
        }
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_invalid_email(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'passw0rd!',
            'email': 'user1111@mail.com',
        }
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_get_profile(self):
        """ Test User Get Profile """
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().get('/api/users/profile',
                                headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('email'), 'user@mail.com')
        self.assertEqual(json_data.get('name'), 'user')

    def test_user_update_profile(self):
        """ Test User Update Profile """
        user1 = {
            'name': 'new name'
        }
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/users/profile',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'new name')

    def test_delete_user(self):
        """ Test User Delete """
        res = self.register(self.user)
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/users/profile',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
