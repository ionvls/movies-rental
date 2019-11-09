import unittest
import json
from src.app import create_app, db
from src.model import GenreModel, MovieModel


class GenreTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.genre = {'name': 'Horror'}
        self.user = {
            'name': 'user',
            'email': 'user@mail.com',
            'password': 'passw0rd!'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()
            g = GenreModel({"name": "Adventure"})
            m = MovieModel({"title": "Star Wars"})
            m.genres.append(g)
            g.save()
            m.save()

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

    def create_genre(self, genre, api_token):
        return self.client().post('/api/genre/', headers={'Content-Type': 'application/json', 'api-token': api_token},
                                  data=json.dumps(genre))

    """
    Test Methods
    """

    def test_genre_create(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        res = self.create_genre(self.genre, api_token)
        self.assertEqual(res.status_code, 201)

    def test_genre_create_with_empty_request(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        genre1 = {}
        res = self.create_genre(genre1, api_token)
        self.assertEqual(res.status_code, 400)

    def test_genre_get_movies(self):
        res = self.client().get('/api/genre/1/movies')
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data[0]['title'], 'Star Wars')

    def test_genre_update(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        genre1 = {
            'name': 'Comedy'
        }
        res = self.create_genre(self.genre, api_token)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/api/genre/1',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(genre1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'Comedy')

    def test_genre_delete(self):
        api_token = self.get_user_login_token()
        self.assertIsNotNone(api_token)
        res = self.create_genre(self.genre, api_token)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/genre/1',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
