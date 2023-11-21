from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from fastapi_cache.decorator import cache

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from .models import Category, Site, News
from .schemas import NewsCreate, NewsUpdate


def pagination_params(
    limit: int = 10,
    skip: int = 0
):
    return {"limit": limit, "skip": skip}


site_router = APIRouter(
    prefix="/site",
    tags=["Site"]
)


@site_router.get("/")
async def get_all_sites(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Site).order_by("title")
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


category_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@category_router.get("/")
async def get_all_categories(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Category).order_by("title")
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get("/")
@cache(expire=30)
async def get_all_news(
    session: AsyncSession = Depends(get_async_session),
    pagination_params: dict = Depends(pagination_params)
):
    try:
        query = select(News).order_by("date")
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


@news_router.post("/")
async def add_news(
    new: NewsCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(News).values(**new.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"message": "Новость успешно добавлена!"}
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


@news_router.get("/id/{news_id}")
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(News).where(News.id == news_id)
    result = await session.execute(query)
    if result.scalar():
        return result.scalar()
    else:
        raise HTTPException(status_code=404, detail="id не существует")


@news_router.patch("/id/{news_id}/update")
async def patch_news_by_id(
    new: NewsUpdate,
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(News).where(News.id == news_id)
        stmt = update(News).values(**new.model_dump()).where(News.id == news_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Новость успешно обновлена!"}
    except Exception as e:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


@news_router.delete("/id/{news_id}/delete")
async def delete_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = delete(News).where(News.id == news_id)
        await session.execute(query)
        await session.commit()
        return {"message": "Новость успешно удалена!"}
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


@news_router.get("/favourites")
async def get_favourite_news(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(News).where(News.is_favourite)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


#здесь можно будет добавить в параметрах свойства юзера для определения наличия/отсуствия роли админа
# current_user = fastapi_users.current_user()
# @app.get("/protected_route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.login}"