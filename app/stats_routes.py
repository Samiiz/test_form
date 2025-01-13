import plotly.express as px
import pandas as pd
from flask import jsonify, Blueprint
from sqlalchemy import func
from config import db
from app.models import Answer, User
from io import BytesIO
import base64

stats_routes = Blueprint('stats_routes', __name__)


@stats_routes.route('/stats/answer_count_by_choice', methods=['GET'])
def answer_count_by_choice():
    result = db.session.query(
        Answer.choice_id, func.count(Answer.id).label('answer_count')
    ).group_by(Answer.choice_id).all()

    df = pd.DataFrame(result, columns=["Choice ID", "Answer Count"])
    fig = px.bar(df, x="Choice ID", y="Answer Count", title="응답 수별 선택지")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/answer_count_by_user', methods=['GET'])
def answer_count_by_user():
    result = db.session.query(
        Answer.user_id, func.count(Answer.id).label('answer_count')
    ).group_by(Answer.user_id).all()

    df = pd.DataFrame(result, columns=["User ID", "Answer Count"])
    fig = px.bar(df, x="User ID", y="Answer Count", title="사용자별 응답 개수")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/response_rate', methods=['GET'])
def response_rate():
    total_users = db.session.query(func.count(User.id)).scalar()
    answered_users = db.session.query(func.count(Answer.user_id.distinct())).scalar()
    response_rate = (answered_users / total_users) * 100

    df = pd.DataFrame({
        "Category": ["응답 완료", "미응답"],
        "Count": [answered_users, total_users - answered_users]
    })

    fig = px.pie(df, values="Count", names="Category", title=f"응답율: {response_rate:.2f}%")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/answer_count_by_question', methods=['GET'])
def answer_count_by_question():
    result = db.session.query(
        Answer.question_id, func.count(Answer.id).label('answer_count')
    ).group_by(Answer.question_id).all()

    df = pd.DataFrame(result, columns=["Question ID", "Answer Count"])
    fig = px.bar(df, x="Question ID", y="Answer Count", title="질문별 응답자 수")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/answer_rate_by_choice', methods=['GET'])
def answer_rate_by_choice():
    total_answers = db.session.query(func.count(Answer.id)).scalar()
    specific_choice_answers = db.session.query(func.count(Answer.id)).filter(Answer.choice_id == 1).scalar()

    choice_response_rate = (specific_choice_answers / total_answers) * 100

    df = pd.DataFrame({
        "Category": ["선택지 1 응답", "기타 선택지 응답"],
        "Count": [specific_choice_answers, total_answers - specific_choice_answers]
    })

    fig = px.pie(df, values="Count", names="Category", title=f"선택지 1 응답률: {choice_response_rate:.2f}%")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/answer_count_by_age', methods=['GET'])
def answer_count_by_age():
    result = db.session.query(
        User.age, func.count(Answer.id).label('answer_count')
    ).join(User, User.id == Answer.user_id).group_by(User.age).all()

    df = pd.DataFrame(result, columns=["Age Group", "Answer Count"])
    fig = px.bar(df, x="Age Group", y="Answer Count", title="연령대별 응답 수")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/most_chosen_choice', methods=['GET'])
def most_chosen_choice():
    result = db.session.query(
        Answer.choice_id, func.count(Answer.id).label('count')
    ).group_by(Answer.choice_id).order_by(func.count(Answer.id).desc()).first()

    df = pd.DataFrame([result], columns=["Choice ID", "Count"])
    fig = px.pie(df, values="Count", names="Choice ID", title="최다 선택된 선택지")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})


@stats_routes.route('/stats/least_chosen_choice', methods=['GET'])
def least_chosen_choice():
    result = db.session.query(
        Answer.choice_id, func.count(Answer.id).label('count')
    ).group_by(Answer.choice_id).order_by(func.count(Answer.id)).first()

    df = pd.DataFrame([result], columns=["Choice ID", "Count"])
    fig = px.pie(df, values="Count", names="Choice ID", title="가장 적게 선택된 선택지")

    # 그래프를 이미지로 변환하여 응답으로 반환
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64})
