from databases import Database

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./pars_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

database = Database(SQLALCHEMY_DATABASE_URL)
