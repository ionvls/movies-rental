# src/model/user_model.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .rental_model import RentalSchema


class UserModel(db.Model):

    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    rentals = db.relationship('RentalModel', backref='users', lazy=True)

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(user_id):
        return UserModel.query.get(user_id)

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    rentals = fields.Nested(RentalSchema, many=True)
