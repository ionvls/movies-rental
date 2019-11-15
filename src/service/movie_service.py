from src.service import custom_response
from ..model.movie_model import MovieModel, MovieSchema

movie_schema = MovieSchema()


class MovieService:

    @staticmethod
    def get_all():
        movies = MovieModel.get_all_movies()
        data = movie_schema.dump(movies, many=True)
        return custom_response(data, 200)

    @staticmethod
    def get_by_title(title: str):
        if not title:
            return custom_response({'error': 'no title provided'}, 400)
        movie = MovieModel.get_by_title(title)
        if not movie:
            return custom_response({'error': 'movie not found'}, 404)
        data = movie_schema.dump(movie, many=True)
        return custom_response(data, 200)

    @staticmethod
    def update(movie_id: int, data):
        movie = MovieModel.get_by_id(movie_id)
        if not movie:
            return custom_response({'error': 'not found'}, 404)

        movie.update(data)

        data = movie_schema.dump(movie)
        return custom_response(data, 200)

    @staticmethod
    def delete_by_id(movie_id: int):
        movie = MovieModel.get_by_id(movie_id)
        if not movie:
            return custom_response({'error': 'movie not found'}, 404)
        movie.delete()
        return custom_response({'message': 'deleted'}, 204)

    @staticmethod
    def create(data):

        movie = MovieModel(data)
        movie.save()
        data = movie_schema.dump(movie)
        return custom_response(data, 201)
