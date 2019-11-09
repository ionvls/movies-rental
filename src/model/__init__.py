# src/model/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()


from .rental_model import RentalModel, RentalSchema
from .user_model import UserModel, UserSchema
from .movie_model import MovieModel, MovieSchema
from .genre_model import GenreModel, GenreSchema
