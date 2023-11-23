import os

from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

AUTH_SECRET = os.environ.get("AUTH_SECRET")
MANAGER_SECRET = os.environ.get("MANAGER_SECRET")

PARS_APP_SITE = os.environ.get("PARS_APP_SITE")