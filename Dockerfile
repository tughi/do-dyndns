FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt \
    && pip install gunicorn

COPY app.py .flaskenv LICENSE ./

CMD gunicorn --bind 0.0.0.0:5000 app:app
