from databases import Database

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


DATABASE_URL = "sqlite+aiosqlite:///./pars_app.db"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# DATABASE_URL = "sqlite:///./pars_app.db"
#
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

database = Database(DATABASE_URL)
