FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
