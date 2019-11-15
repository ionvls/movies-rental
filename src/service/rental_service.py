from flask import g

from src.model.movie_model import MovieSchema
from src.model.rental_model import RentalModel, RentalSchema
from marshmallow import ValidationError
from src.service import custom_response

rental_schema = RentalSchema()
movie_schema = MovieSchema()


class RentalService:

    @staticmethod
    def get_user():
        return g.user.get('id')

    @staticmethod
    def create(req_data):

        req_data['user_id'] = RentalService.get_user()
        try:
            data = rental_schema.load(req_data)
        except ValidationError as e:
            return custom_response(e.messages, 400)
        rental = RentalModel(data)
        rental.save()
        data = rental_schema.dump(rental)
        return custom_response(data, 201)

    @staticmethod
    def get_by_id(rental_id: int):

        rental = RentalModel.get_by_id(rental_id)
        if not rental:
            return custom_response({'error': 'not found'}, 404)
        data = rental_schema.dump(rental)
        if data.get('user_id') != RentalService.get_user():
            return custom_response({'error': 'permission denied'}, 400)
        return custom_response(data, 200)

    @staticmethod
    def get_all():

        rentals = RentalModel.get_all_rentals()
        data = rental_schema.dump(rentals, many=True)
        return custom_response(data, 200)

    @staticmethod
    def update(rental_id: int, req_data):

        rental = RentalModel.get_by_id(rental_id)
        if not rental:
            return custom_response({'error': 'not found'}, 404)
        data = rental_schema.dump(rental)
        if data.get('user_id') != RentalService.get_user():
            return custom_response({'error': 'permission denied'}, 400)

        try:
            data = rental_schema.load(req_data, partial=True)
        except ValidationError as e:
            return custom_response(e.messages, 400)
        rental.update(data)

        data = rental_schema.dump(rental)
        return custom_response(data, 200)

    @staticmethod
    def delete_by_id(rental_id: int):

        rental = RentalModel.get_by_id(rental_id)
        if not rental:
            return custom_response({'error': 'rental not found'}, 404)
        data = rental_schema.dump(rental)
        if data.get('user_id') != RentalService.get_user():
            return custom_response({'error': 'permission denied'}, 400)

        rental.delete()
        return custom_response({'message': 'deleted'}, 204)

    @staticmethod
    def return_movie(req_data):

        rental = RentalModel.get_by_id(req_data["rental_id"])
        if not rental:
            return custom_response({'error': 'rental not found'}, 404)
        data = rental_schema.dump(rental)
        if data.get('user_id') != RentalService.get_user():
            return custom_response({'error': 'permission denied'}, 400)
        rental = rental.return_movie()

        data = rental_schema.dump(rental)
        return custom_response(data, 200)
