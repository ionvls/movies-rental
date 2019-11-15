# /src/controller/UserView

from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource

from src.service.user_service import UserService
from ..model.user_model import UserSchema
from ..shared.Authentication import Auth

user_api = Namespace("User", description="User information")


@user_api.route('/register')
class UserRegisterResource(Resource):

    @accepts(schema=UserSchema, api=user_api)
    @responds(schema=UserSchema)
    def post(self):
        """Register"""
        return UserService.create(request.parsed_obj)


@user_api.route('/profile')
class UserProfileResource(Resource):

    @accepts(schema=UserSchema(partial=True), api=user_api)
    @responds(schema=UserSchema)
    @Auth.auth_required
    def put(self):
        """Update user"""
        return UserService.update(request.parsed_obj)

    @Auth.auth_required
    def delete(self):
        """Delete current User"""
        return UserService.delete()

    @responds(schema=UserSchema)
    @Auth.auth_required
    def get(self):
        """Get logged in user"""
        return UserService.get_logged_in_user()


@user_api.route('/login')
class UserLoginResource(Resource):

    @accepts(schema=UserSchema(partial=True), api=user_api)
    def post(self):
        """Login User"""
        return UserService.login(request.parsed_obj)
