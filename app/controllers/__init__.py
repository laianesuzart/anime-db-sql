from flask import Flask


def init_app(app: Flask):
    from .animes_controller import bp_animes
    app.register_blueprint(bp_animes)

    return app
