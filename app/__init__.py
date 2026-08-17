from flask import Flask
from config import Config

from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app import models

    with app.app_context():
        db.create_all()

    from app.controllers import main_controller, student_controller, course_controller

    app.register_blueprint(main_controller)
    app.register_blueprint(student_controller)
    app.register_blueprint(course_controller)
    
    return app