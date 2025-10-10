from flask import Flask


def create_app(config_object=None):
    """Simple app factory to ensure 'app' is a package and provide a start point.

    This file exists mainly so imports like `from app.database.connection import db` work
    when running the app as a package or from an IDE.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if config_object:
        app.config.from_object(config_object)

    return app
