FROM python:3.10

RUN mkdir /parsing_application

WORKDIR parsing_application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000