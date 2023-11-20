from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category, Site, News
from src.database import get_async_session


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




