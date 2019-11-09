import unittest

from src.model.movie_model import MovieModel
from src.model.user_model import UserModel
from src.model.rental_model import RentalModel
from src.app import create_app, db
from datetime import datetime
from unittest.mock import Mock, patch

rent_day = datetime(year=2019, month=1, day=1, hour=1)
day0 = datetime(year=2019, month=1, day=1, hour=3)
day2 = datetime(year=2019, month=1, day=3)
day3 = datetime(year=2019, month=1, day=4)
day4 = datetime(year=2019, month=1, day=5)
day5 = datetime(year=2019, month=1, day=6)

datetime = Mock()


class RentalModelTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = UserModel({'name': 'user', 'email': 'user@mail.com', 'password': 'passw0rd!'})
        self.movie = MovieModel({'title': 'Star Wars'})
        with self.app.app_context():
            # create all tables
            db.create_all()
            self.user.save()
            self.movie.save()

    def create_rental(self):
        rental = RentalModel({'user_id': 1, 'movie_id': 1})
        db.session.add(rental)
        db.session.commit()
        return rental

    @patch('src.model.RentalModel.get_now')
    def test_return_same_day(self, mock_now):
        mock_now.return_value = rent_day
        rental = self.create_rental()
        self.assertIsNotNone(rental)
        mock_now.return_value = day0
        rental.return_movie()
        self.assertEqual(1, rental.fee)
        self.assertEqual(day0, rental.returned_at)

    @patch('src.model.RentalModel.get_now')
    def test_return_after_two_days(self, mock_now):
        mock_now.return_value = rent_day
        rental = self.create_rental()
        self.assertIsNotNone(rental)
        mock_now.return_value = day2
        rental.return_movie()
        self.assertEqual(2, rental.fee)
        self.assertEqual(day2, rental.returned_at)

    @patch('src.model.RentalModel.get_now')
    def test_return_after_three_days(self, mock_now):
        mock_now.return_value = rent_day
        rental = self.create_rental()
        self.assertIsNotNone(rental)
        mock_now.return_value = day3
        rental.return_movie()
        self.assertEqual(3, rental.fee)
        self.assertEqual(day3, rental.returned_at)

    @patch('src.model.RentalModel.get_now')
    def test_return_after_four_days(self, mock_now):
        mock_now.return_value = rent_day
        rental = self.create_rental()
        self.assertIsNotNone(rental)
        mock_now.return_value = day4
        rental.return_movie()
        self.assertEqual(3.5, rental.fee)
        self.assertEqual(day4, rental.returned_at)

    @patch('src.model.RentalModel.get_now')
    def test_return_after_five_days(self, mock_now):
        mock_now.return_value = rent_day
        rental = self.create_rental()
        self.assertIsNotNone(rental)
        mock_now.return_value = day5
        rental.return_movie()
        self.assertEqual(4, rental.fee)
        self.assertEqual(day5, rental.returned_at)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
