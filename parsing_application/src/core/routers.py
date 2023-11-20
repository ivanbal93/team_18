from fastapi import APIRouter, Depends

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category, Site, News
from src.database import get_async_session
from .schemas import NewsCreate

site_router = APIRouter(
    prefix="/site",
    tags=["Site"]
)


@site_router.get("/")
async def get_all_sites(session: AsyncSession = Depends(get_async_session)):
    query = select(Site).order_by("title")
    result = await session.execute(query)
    return result.scalars().all()


category_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@category_router.get("/")
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    query = select(Category).order_by("title")
    result = await session.execute(query)
    return result.scalars().all()


news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get("/")
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    query = select(News).order_by("title")
    result = await session.execute(query)
    return result.scalars().all()


@news_router.post("/")
async def add_news(new: NewsCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(News).values(**new.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"message": "Новость успешно добавлена!"}




