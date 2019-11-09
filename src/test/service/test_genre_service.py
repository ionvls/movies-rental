import unittest
import json
from typing import List

from src.app import create_app, db
from src.model.genre_model import GenreModel, GenreSchema
from src.service.genre_service import GenreService
from src.model.movie_model import MovieModel, MovieSchema

movie_schema = MovieSchema()
genre_schema = GenreSchema()


class GenreTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.genre1 = {'name': 'Horror'}
        self.genre2 = {'name': 'Comedy'}
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_genre_create(self):
        res = GenreService.create(genre_schema.load(self.genre1))

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_data['name'], 'Horror')

        res = GenreService.get_all()

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 1)

    def test_genre_get_movies(self):
        genre = GenreModel(genre_schema.load(self.genre1))
        genre.save()
        movie = MovieModel(movie_schema.load({'title': 'ScaryMovie'}))
        movie.genres.append(genre)
        movie.save()

        res = GenreService.get_movies(1)

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(json_data, List)
        self.assertEqual(json_data.__len__(), 1)
        self.assertEqual(json_data[0]['title'], 'ScaryMovie')

    def test_genre_get_all(self):
        genre = GenreModel(genre_schema.load(self.genre1))
        genre.save()
        genre = GenreModel(genre_schema.load(self.genre2))
        genre.save()

        res = GenreService.get_all()

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 2)

    def test_genre_update(self):
        genre = GenreModel(genre_schema.load(self.genre1))
        genre.save()

        res = GenreService.update(1, genre_schema.load(self.genre2))

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'Comedy')

    def test_delete_genre(self):
        genre = GenreModel(genre_schema.load(self.genre1))
        genre.save()

        res = GenreService.delete_by_id(1)
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
