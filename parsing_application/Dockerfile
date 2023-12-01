FROM python:3.10

RUN mkdir /parsing_application

WORKDIR parsing_application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade 'f0ba6ccfd9f1'

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000