FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD python3 migrate.py && python3 -m flask run --host=0.0.0.0 --port=8080
