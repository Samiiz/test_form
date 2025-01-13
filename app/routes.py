from flask import (Blueprint, request, jsonify, session)
from app.services import users, images, questions, choices, answers

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


@routes.route("/image", methods=["GET", "POST"])
def create_image():
    if request.method == "POST":
        try:
            image = images.create_image()
            return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201
        
        except ValueError:
            return jsonify({"message": "error"}), 400


@routes.route("/question", methods=["GET", "POST"])
def create_questions():
    if request.method == "POST":
        try:
            question = questions.create_question()
            return jsonify({"message": f"Title: {question.title} question Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400


@routes.route("/choice", methods=["GET", "POST"])
def create_choice():
    if request.method == "POST":
        try:
            choice = choices.create_choice()
            return jsonify({"message": f"Content: {choice.content} choice Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400

@routes.route("/answer", methods=["GET", "POST"])
def create_answer():
    if request.method == "POST":
        try:
            answer = answers.create_answer()
            return jsonify({"message": f"User: {answer.user_id}'s answer Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400