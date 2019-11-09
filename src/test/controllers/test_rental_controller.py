import json
import unittest

from src.app import create_app, db


class RentalTest(unittest.TestCase):

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

    def create_user_and_movie(self):
        res = self.client().post('/api/users/register', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        res = self.client().post('/api/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        user_data = json.loads(res.data)
        api_token = user_data.get('jwt_token')
        res = self.client().post('/api/movie/', headers={'Content-Type': 'application/json', 'api-token': api_token},
                                 data=json.dumps(self.movie))
        movie_data = json.loads(res.data)
        rental = {'movie_id': movie_data.get('id')}
        return api_token, rental

    def create_rental(self, api_token, rental):
        return self.client().post('/api/rental/', headers={'Content-Type': 'application/json', 'api-token': api_token},
                                  data=json.dumps(rental))

    """
    Test Methods
    """

    def test_rental_create(self):
        api_token, rental = self.create_user_and_movie()
        self.assertIsNotNone(api_token)
        self.assertIsNotNone(rental)

        res = self.create_rental(api_token, rental)
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_data.get('fee'), 0)

    def test_rental_create_with_empty_request(self):
        api_token, rental = self.create_user_and_movie()
        self.assertIsNotNone(api_token)
        self.assertIsNotNone(rental)

        rental1 = {}
        res = self.create_rental(api_token, rental1)
        self.assertEqual(res.status_code, 400)

    def test_rental_get_by_id(self):
        api_token, rental = self.create_user_and_movie()
        self.assertIsNotNone(api_token)
        self.assertIsNotNone(rental)

        res = self.create_rental(api_token, rental)
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/api/rental/1', headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('fee'), 0)

    def test_rental_update(self):
        api_token, rental = self.create_user_and_movie()
        self.assertIsNotNone(api_token)
        self.assertIsNotNone(rental)

        """ create second movie """
        res = self.client().post('/api/movie/', headers={'Content-Type': 'application/json', 'api-token': api_token},
                                 data=json.dumps({'title': 'Singularity'}))
        movie_id = json.loads(res.data).get('id')
        rental1 = {
            'movie_id': movie_id
        }
        res = self.create_rental(api_token, rental)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/api/rental/1',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(rental1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('movie_id'), 2)

    def test_delete_rental(self):
        api_token, rental = self.create_user_and_movie()
        self.assertIsNotNone(api_token)
        self.assertIsNotNone(rental)

        res = self.create_rental(api_token, rental)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/rental/1',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
