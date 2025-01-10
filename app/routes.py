from flask import (Blueprint, request, jsonify, session)
from app.views import users


routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def connect():
    if request.method == 'GET':
        return jsonify({"message": "Success Connect"})

@routes.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        try:
            user = users.create_user()
            session["user_id"] = user.id
            return jsonify({"message": f"{user.name}님 회원가입을 축하합니다"}), 201

        except ValueError:
            return jsonify({"message": "이미 존재하는 계정 입니다."}), 400

