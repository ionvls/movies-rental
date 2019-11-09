# src/model/movie_model.py
from marshmallow import fields, Schema

from src.model.genre_model import GenreSchema
from . import db

secondary_table = db.Table('movie_genres',
                           db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
                           db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True))


class MovieModel(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    genres = db.relationship('GenreModel', secondary=secondary_table, backref=db.backref('movies', lazy=True), lazy="subquery")

    # class constructor
    def __init__(self, data):
        self.title = data.get('title')

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
    def get_all_movies():
        return MovieModel.query.all()

    @staticmethod
    def get_by_id(rental_id):
        return MovieModel.query.get(rental_id)

    @staticmethod
    def get_by_title(title):
        return MovieModel.query.filter_by(title=title).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    genres = fields.Nested(GenreSchema, many=True)
