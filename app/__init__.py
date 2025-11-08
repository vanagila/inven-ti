from flask import Flask

def create_app(config_object=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if config_object:
        app.config.from_object(config_object)

    return app
