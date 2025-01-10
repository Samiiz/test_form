#!/bin/bash

set -e  # 오류 발생 시 즉시 종료

# 오류 발생 시 오류 메시지를 출력하는 함수
trap 'echo "Error occurred in script at line $LINENO"; exit 1' ERR

echo "==== Flask Migration ===="
echo

# 가상환경 활성화
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Please ensure '.venv' exists."
    exit 1
fi

# Flask 마이그레이션 작업
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

echo "==== Migration Completed ===="

