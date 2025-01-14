from flask import jsonify, Blueprint
from sqlalchemy import func
from config import db
from app.models import Answer, Question, Choices

stats_routes = Blueprint('stats_routes', __name__)


@stats_routes.route('/stats/answer_count_by_choice', methods=['GET'])
def answer_count_by_question():
    # 쿼리 작성하여 데이터 가져오기
    query = db.session.query(
        Question.title,
        Choices.content,
        func.count(Answer.id).label('answer_count'),
        func.count(Answer.id) / func.sum(func.count(Answer.id)).over(partition_by=[Question.id]).label('percentage')
    ) \
    .join(Choices, Choices.id == Answer.choice_id) \
    .join(Question, Question.id == Choices.question_id) \
    .group_by(Question.id, Choices.id) \
    .all()

    data = []
    for row in query:
        data.append({
            "title": row.title,
            "choices": [row.content],
            "percentage": [row.percentage * 100],  # 백분율로 변환
        })

    return jsonify(data)