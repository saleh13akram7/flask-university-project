from flask import Flask
from config import Config

from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    from .controllers import main_controller

    app.register_blueprint(main_controller)

    return app