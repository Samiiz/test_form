from flask import Flask
from flask_migrate import Migrate

import app.models
from app.routes import routes
from app.stats_routes import stats_routes
from config import db

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

    # 블루 프린트 등록
    application.register_blueprint(routes)
    application.register_blueprint(stats_routes)


    return application
