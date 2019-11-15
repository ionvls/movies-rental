# /src/controller/genre_controller.py
from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource

from ..model.genre_model import GenreSchema
from ..model.movie_model import MovieSchema
from ..service.genre_service import GenreService
from ..shared.Authentication import Auth

genre_api = api = Namespace("Genre", description="Genre information")


@genre_api.route('/')
class GenreResource(Resource):

    @accepts(schema=GenreSchema, api=genre_api)
    @responds(schema=GenreSchema)
    @Auth.auth_required
    def post(self):
        """Create Genre"""
        return GenreService.create(request.parsed_obj)

    @responds(schema=GenreSchema(many=True))
    def get(self):
        """Get all Genres"""
        return GenreService.get_all()


@genre_api.route('/<genre_id>')
class GenreIdResource(Resource):

    @accepts(schema=GenreSchema(partial=True), api=genre_api)
    @responds(schema=GenreSchema)
    @Auth.auth_required
    def put(self, genre_id: int):
        """Update Genre"""
        return GenreService.update(genre_id, request.parsed_obj)

    @Auth.auth_required
    def delete(self, genre_id: int):
        """Delete Genre"""
        return GenreService.delete_by_id(genre_id)


@genre_api.route('/<genre_id>/movies')
class GenreIdMoviesResource(Resource):

    @responds(schema=MovieSchema(many=True))
    def get(self, genre_id: int):
        """Get movies by Genre"""
        return GenreService.get_movies(genre_id)
