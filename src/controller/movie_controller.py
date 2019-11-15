# /src/controller/movie_controller.py
from flask import request
from flask_accepts import responds, accepts
from flask_restplus import Namespace, Resource

from src.service.movie_service import MovieService
from ..model.movie_model import MovieSchema
from ..shared.Authentication import Auth

movie_api = Namespace("Movie", description="Movie information")


@movie_api.route('/')
class MovieResource(Resource):

    @accepts(schema=MovieSchema, api=movie_api)
    @responds(schema=MovieSchema)
    @Auth.auth_required
    def post(self):
        """Create Movie"""
        return MovieService.create(request.parsed_obj)

    @responds(schema=MovieSchema(many=True))
    def get(self):
        """Get all movies"""
        return MovieService.get_all()


@movie_api.route('/search')
class MovieSearch(Resource):

    @movie_api.param('title', 'Movie title')
    @responds(schema=MovieSchema(many=True))
    def post(self):
        """Search by title"""
        req_data = request.json
        return MovieService.get_by_title(req_data['title'])


@movie_api.route('/<movie_id>')
class MovieIdResource(Resource):

    @accepts(schema=MovieSchema(partial=True), api=movie_api)
    @responds(schema=MovieSchema)
    @Auth.auth_required
    def put(self, movie_id: int):
        """Update Move"""
        return MovieService.update(movie_id, request.parsed_obj)

    @Auth.auth_required
    def delete(self, movie_id: int):
        """Delete Movie"""
        return MovieService.delete_by_id(movie_id)
