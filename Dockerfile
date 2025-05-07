FROM python:3.12.3-slim

WORKDIR /app

ENV BASE_URL=http://0.0.0.0:11435

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
