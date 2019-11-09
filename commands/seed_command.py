from flask_script import Command

from src.model import db
from src.model.movie_model import MovieModel
from src.model.user_model import UserModel
from src.model.genre_model import GenreModel


def seed_things():

    genre_names = [
        {"name": "Horror"},
        {"name": "Action"},
        {"name": "Romance"},
        {"name": "Comedy"},
        {"name": "Adventure"}
    ]
    genres = []
    for genre in genre_names:
        g = GenreModel(genre)
        g.save()
        genres.append(g)

    m = MovieModel({"title": "Saw"})
    m.genres.extend([genres[0], genres[3]])
    m.save()

    m = MovieModel({"title": "Hitman"})
    m.genres.append(genres[1])
    m.save()

    m = MovieModel({"title": "Notebook"})
    m.genres.append(genres[2])
    m.save()

    m = MovieModel({"title": "Star Wars"})
    m.genres.extend([genres[1], genres[4]])
    m.save()

    users = [
            {"name": "user1", "email": "user1@mail.com", "password": "1234"},
            {"name": "user2", "email": "user2@mail.com", "password": "1234"},
    ]
    for user in users:
        u = UserModel(user)
        u.save()


class SeedCommand(Command):
    """ Seed the DB."""

    def run(self):
        if (
            input(
                "Are you sure you want to drop all tables and recreate? (y/N)\n"
            ).lower()
            == "y"
        ):
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            seed_things()
            db.session.commit()
            print("DB successfully seeded.")
