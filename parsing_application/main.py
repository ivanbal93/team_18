import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from fastapi_users import fastapi_users, FastAPIUsers

from authentication.auth import auth_backend
from authentication.database_config import User
from authentication.manager import get_user_manager
from authentication.schemas import UserRead, UserCreate

from database_config import database


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="Parsing Application"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)


@app.on_event("startup")
async def startup_database():
    '''Подключение к БД'''
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    '''Отключение от БД'''
    await database.disconnect()


@app.get("/")
def hello_world():
    return "Hello, World!"
