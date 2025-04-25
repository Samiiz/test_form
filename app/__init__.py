from flask import Flask, jsonify
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

    @application.errorhandler(400)
    def handle_bad_request(error):
        response = jsonify({"message": error.description})  # JSON 형식 응답
        response.status_code = 400
        return response

    # 블루 프린트 등록
    application.register_blueprint(routes)
    application.register_blueprint(stats_routes)


    return application
