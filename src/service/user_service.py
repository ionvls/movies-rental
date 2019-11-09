from flask import g

from src.model.user_model import UserModel, UserSchema
from marshmallow import ValidationError

from src.shared.Authentication import Auth
from src.service import custom_response

user_schema = UserSchema()

class UserService:

    @staticmethod
    def get_user():
        return g.user.get('id')

    @staticmethod
    def create(data):

        user_in_db = UserModel.get_user_by_email(data.get('email'))
        if user_in_db:
            message = {'error': 'User already exist, please supply another email address'}
            return custom_response(message, 400)

        user = UserModel(data)
        user.save()
        ser_data = user_schema.dump(user)
        token = Auth.generate_token(ser_data.get('id'))
        return custom_response({'jwt_token': token}, 201)

    @staticmethod
    def get_logged_in_user():

        user = UserModel.get_one_user(UserService.get_user())
        ser_user = user_schema.dump(user)
        return custom_response(ser_user, 200)

    @staticmethod
    def update(data):

        user = UserModel.get_one_user(UserService.get_user())
        user.update(data)
        ser_user = user_schema.dump(user)
        return custom_response(ser_user, 200)

    @staticmethod
    def delete():

        user = UserModel.get_one_user(UserService.get_user())
        user.delete()
        return custom_response({'message': 'deleted'}, 204)

    @staticmethod
    def login(data):

        if not data.get('email') or not data.get('password'):
            return custom_response({'error': 'you need email and password to sign in'}, 400)
        user = UserModel.get_user_by_email(data.get('email'))
        if not user:
            return custom_response({'error': 'invalid credentials'}, 400)
        if not user.check_hash(data.get('password')):
            return custom_response({'error': 'invalid credentials'}, 400)
        ser_data = user_schema.dump(user)
        token = Auth.generate_token(ser_data.get('id'))
        return custom_response({'jwt_token': token}, 200)
