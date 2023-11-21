import uvicorn

from redis import asyncio as aioredis

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.authentication.config import auth_backend, fastapi_users
from src.authentication.schemas import UserRead, UserCreate

from src.core.routers import site_router, category_router, news_router
from src.database import database

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)

app = FastAPI(
    title="Parsing Application"
)

# Настройка CORS
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT",],
    allow_headers=["Access-Control-Allow-Headers", "Access-Control-Allow-Origin",],
)

# Подключение маршрутов
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(site_router)
app.include_router(category_router)
app.include_router(news_router)


# Кеширование
@app.on_event("startup")
async def startup():
    await database.connect()
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()