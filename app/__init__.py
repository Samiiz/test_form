from config import db
from flask import Flask
from flask_migrate import Migrate
from app.routes import routes
import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

    # 블루 프린트 등록
    application.register_blueprint(routes)

    return application

