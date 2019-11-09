import unittest
import json
from src.app import create_app, db
from src.model.movie_model import MovieModel, MovieSchema
from src.service.movie_service import MovieService

movie_schema = MovieSchema()


class MovieTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.movie1 = {'title': 'Star Wars'}
        self.movie2 = {'title': 'Singularity'}
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_movie_create(self):
        res = MovieService.create(movie_schema.load(self.movie1))

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_data['title'], 'Star Wars')

        res = MovieService.get_all()

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 1)

    def test_movie_get_by_title(self):
        movie = MovieModel(movie_schema.load(self.movie1))
        movie.save()

        res = MovieService.get_by_title(movie.title)

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data[0]['title'], 'Star Wars')

    def test_movie_get_all(self):
        movie = MovieModel(movie_schema.load(self.movie1))
        movie.save()
        movie = MovieModel(movie_schema.load(self.movie2))
        movie.save()

        res = MovieService.get_all()

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.__len__(), 2)

    def test_movie_update(self):
        movie = MovieModel(movie_schema.load(self.movie1))
        movie.save()

        res = MovieService.update(1, movie_schema.load(self.movie2))

        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('title'), 'Singularity')

    def test_delete_movie(self):
        movie = MovieModel(movie_schema.load(self.movie1))
        movie.save()

        res = MovieService.delete_by_id(1)
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
