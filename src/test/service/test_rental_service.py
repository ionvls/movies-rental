import unittest
import json
from typing import List

from unittest.mock import patch

from src.app import create_app, db
from src.model import UserModel, UserSchema
from src.model.rental_model import RentalModel, RentalSchema
from src.service.rental_service import RentalService
from src.model.movie_model import MovieModel, MovieSchema

movie_schema = MovieSchema()
user_schema = UserSchema()
rental_schema = RentalSchema()


class RentalTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user1 = {
            'name': 'user',
            'email': 'user@mail.com',
            'password': 'passw0rd!'
        }
        self.rental1 = {'movie_id': 1, 'user_id': 1}
        with self.app.app_context():
            # create all tables
            db.create_all()
            movie = MovieModel(movie_schema.load({'title': 'test'}))
            movie.save()
            user = UserModel(user_schema.load(self.user1))
            user.save()

    @patch.object(RentalService, 'get_user', lambda: 1)
    def test_rental_create(self):
        #fail first
        res = RentalService.create(rental_schema.load({}, partial=True))
        self.assertEqual(res.status_code, 400)

        res = RentalService.create(rental_schema.load({'movie_id': 1}, partial=True))
        self.assertEqual(res.status_code, 201)

        res = RentalService.get_all()
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 1)

    @patch.object(RentalService, 'get_user', lambda: 1)
    def test_rental_get_by_id(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.get_by_id(13)
        self.assertEqual(res.status_code, 404)

        res = RentalService.get_by_id(1)

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('movie_id'), 1)

    @patch.object(RentalService, 'get_user', lambda: 2)
    def test_rental_get_by_id_without_permission(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.get_by_id(1)
        self.assertEqual(res.status_code, 400)

    def test_rental_get_all(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()
        res = RentalService.get_all()

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 2)

    @patch.object(RentalService, 'get_user', lambda: 1)
    def test_rental_update_not_found(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.update(33, rental_schema.load({}, partial=True))
        self.assertEqual(res.status_code, 404)

    @patch.object(RentalService, 'get_user', lambda: 33)
    def test_rental_update_without_permission(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.update(1, rental_schema.load({}, partial=True))
        self.assertEqual(res.status_code, 400)

    @patch.object(RentalService, 'get_user', lambda: 1)
    def test_rental_delete_by_id(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.delete_by_id(1234)
        self.assertEqual(res.status_code, 404)

        res = RentalService.delete_by_id(1)
        self.assertEqual(res.status_code, 204)

    @patch.object(RentalService, 'get_user', lambda: 33)
    def test_rental_delete_by_id_no_permission(self):
        rental = RentalModel(rental_schema.load(self.rental1))
        rental.save()

        res = RentalService.delete_by_id(1)
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
