FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir app

WORKDIR /app

COPY requirements.txt /app
COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

CMD ["bash"]