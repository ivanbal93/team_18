import uvicorn

from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from env_config import REDIS_HOST, REDIS_PORT, PARS_APP_SITE
from src.authentication.config import auth_backend, fastapi_users
from src.authentication.routers import user_router
from src.authentication.schemas import UserRead, UserCreate

from src.core.routers import site_router, category_router, news_router


# if __name__ == "__main__":
#     uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)

app = FastAPI(
    title="Parsing Application"
)

# Настройка CORS
origins = [
    PARS_APP_SITE,
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
app.include_router(user_router)


# Кеширование
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
