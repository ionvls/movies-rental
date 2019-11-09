import unittest
import json
from src.app import create_app, db


class MovieTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.movie = {'title': 'Star Wars'}
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

    def get_user_login_token(self):
        res = self.client().post('/api/users/register', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        res = self.client().post('/api/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        api_token = json.loads(res.data).get('jwt_token')
        return api_token

    def create_movie(self, movie, api_token):
        return self.client().post('/api/movie/', headers={'Content-Type': 'application/json', 'api-token': api_token},
                                  data=json.dumps(movie))

    """
    Test Methods
    """

    def test_movie_create(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        res = self.create_movie(self.movie, api_token)
        self.assertEqual(res.status_code, 201)

    def test_movie_create_with_empty_request(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        movie1 = {}
        res = self.create_movie(movie1, api_token)
        self.assertEqual(res.status_code, 400)

    def test_movie_get_by_title(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        res = self.create_movie(self.movie, api_token)
        self.assertEqual(res.status_code, 201)

        res = self.client().post('/api/movie/search', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.movie))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data[0]['title'], 'Star Wars')

    def test_movie_update(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        movie1 = {
            'title': 'Singularity'
        }
        res = self.create_movie(self.movie, api_token)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/api/movie/1',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(movie1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('title'), 'Singularity')

    def test_delete_movie(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        res = self.create_movie(self.movie, api_token)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/movie/1',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
