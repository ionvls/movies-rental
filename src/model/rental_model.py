# src/model/rental_model.py
from datetime import datetime

from marshmallow import fields, Schema

from . import db
from .movie_model import MovieSchema


class RentalModel(db.Model):

    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fee = db.Column(db.Numeric(10, 2), default=0)
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.id'))
    movie = db.relationship('MovieModel', backref='rental', lazy=True)
    rented_at = db.Column(db.DateTime)
    returned_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.movie_id = data.get('movie_id')
        self.fee = 0
        self.rented_at = self.get_now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_rentals():
        return RentalModel.query.all()

    @staticmethod
    def get_by_id(rental_id):
        return RentalModel.query.get(rental_id)

    def return_movie(self):
        if self.rented_at is not None:
            return_date = self.get_now()
            fee = self.__calculate_fee(return_date)
            self.fee = fee
            self.returned_at = return_date
            db.session.commit()

    def __calculate_fee(self, return_date: datetime):
        days = (return_date - self.rented_at).days + 1
        if days > 3:
            return (days - 3) * .5 + 3
        return days

    @staticmethod
    def get_now():
        return datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class RentalSchema(Schema):

    id = fields.Int(dump_only=True)
    movie_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    fee = fields.Float(dump_only=True)
    rented_at = fields.DateTime(dump_only=True)
    returned_at = fields.DateTime(dump_only=True)
    movie = fields.Nested(MovieSchema, many=False, dump_only=True)
