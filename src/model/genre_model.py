# src/model/genre_model.py
from . import db
from marshmallow import fields, Schema


class GenreModel(db.Model):

    __tablename__ = "genres"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')

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

    def get_movies(self):
        return self.movies

    @staticmethod
    def get_all_genres():
        return GenreModel.query.all()

    @staticmethod
    def get_by_id(rental_id):
        return GenreModel.query.get(rental_id)

    @staticmethod
    def get_by_name(name):
        return GenreModel.query.filter_by(name=name).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class GenreSchema(Schema):

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
