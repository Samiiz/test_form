from flask import request

from config import db

from app.models import Answer


def create_answer(data):
    answer = Answer(
        user_id=data['user_id'],
        choice_id=data['choice_id'],
    )
    db.session.add(answer)
    db.session.commit()

    return answer
