# /src/controller/rental_controller.py

from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource

from ..model.rental_model import RentalModel, RentalSchema
from ..shared.Authentication import Auth
from src.service.rental_service import RentalService

rental_api = Namespace("Rental", description="Rental information")


@rental_api.route('/')
class RentalResource(Resource):

    @rental_api.param('movie_id', 'Movie Id to rent')
    @responds(schema=RentalSchema)
    @Auth.auth_required
    def post(self):
        """Rent Movie (Create Rental)"""
        req_data = request.get_json()
        return RentalService.create(req_data)

    @responds(schema=RentalSchema(many=True))
    @Auth.auth_required
    def get(self):
        """Get all Rentals"""
        return RentalService.get_all()


@rental_api.route('/<rental_id>')
class RentalIdResource(Resource):

    @responds(schema=RentalSchema)
    @Auth.auth_required
    def get(self, rental_id: int):
        """Get Rental by Id"""
        return RentalService.get_by_id(rental_id)

    @responds(schema=RentalSchema)
    @Auth.auth_required
    def put(self, rental_id: int):
        """Update Rental"""
        req_data = request.get_json()
        return RentalService.update(rental_id, req_data)


    @Auth.auth_required
    def delete(self, rental_id: int):
        """Delete Rental"""
        return RentalService.delete_by_id(rental_id)


@rental_api.route('/return')
class RentalReturnResource(Resource):

    @responds(schema=RentalSchema)
    @Auth.auth_required
    def post(self):
        """Return Movie"""
        req_data = request.get_json()
        return RentalService.return_movie(req_data)
