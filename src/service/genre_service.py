from src.model.movie_model import MovieSchema
from src.model.genre_model import GenreModel, GenreSchema
from marshmallow import ValidationError
from src.service import custom_response

genre_schema = GenreSchema()
movie_schema = MovieSchema()


class GenreService:

    @staticmethod
    def get_all():
        genres = GenreModel.get_all_genres()
        data = genre_schema.dump(genres, many=True)
        return custom_response(data, 200)

    @staticmethod
    def get_movies(genre_id: int):
        genre = GenreModel.get_by_id(genre_id)
        if not genre:
            return custom_response({'error': 'not found'}, 404)
        data = movie_schema.dump(genre.movies, many=True)
        return custom_response(data, 200)

    @staticmethod
    def update(genre_id: int, data):
        genre = GenreModel.get_by_id(genre_id)
        if not genre:
            return custom_response({'error': 'not found'}, 404)

        genre.update(data)

        data = genre_schema.dump(genre)
        return custom_response(data, 200)

    @staticmethod
    def delete_by_id(genre_id: int):
        genre = GenreModel.get_by_id(genre_id)
        if not genre:
            return custom_response({'error': 'genre not found'}, 404)

        genre.delete()
        return custom_response({'message': 'deleted'}, 204)

    @staticmethod
    def create(data):

        genre = GenreModel(data)
        genre.save()
        data = genre_schema.dump(genre)
        return custom_response(data, 201)
