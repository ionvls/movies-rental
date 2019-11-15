# src/app.py

from flask import Flask
from flask_restplus import Api

from .config import app_config
from .model import db, bcrypt

# import user_api blueprint
# from .controller.UserController import user_api as user_blueprint
# from .controller.RentalController import rental_api as rental_blueprint
# from .controller.MovieController import movie_api as movie_blueprint
# from .controller.GenreController import genre_api as genre_blueprint


def create_app(env_name):

    from src.routes import register_routes
    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.app_context().push()
    api = Api(app)
    register_routes(api)

    # initializing bcrypt and db
    bcrypt.init_app(app)
    db.init_app(app)

    # app.register_blueprint(user_blueprint, url_prefix='/api/users')
    # app.register_blueprint(rental_blueprint, url_prefix='/api/rental')
    # app.register_blueprint(movie_blueprint, url_prefix='/api/movie')
    # app.register_blueprint(genre_blueprint, url_prefix='/api/genre')

    @app.route('/health', methods=['GET'])
    def index():
        return 'Healthy'

    return app
