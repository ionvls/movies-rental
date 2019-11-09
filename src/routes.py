def register_routes(api, app, root="/api"):
    from .controller.genre_controller import genre_api
    from .controller.movie_controller import movie_api
    from .controller.rental_controller import rental_api
    from .controller.user_controller import user_api

    # Add routes
    api.add_namespace(genre_api, path=f"{root}/genre")
    api.add_namespace(movie_api, path=f"{root}/movie")
    api.add_namespace(rental_api, path=f"{root}/rental")
    api.add_namespace(user_api, path=f"{root}/users")

