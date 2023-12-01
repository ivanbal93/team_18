import os
import json

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.config import current_user_is_auth
from src.authentication.models import User
from src.database import get_async_session
from src.core.category.schemas import CategoryCreate
from src.core.news.schemas import NewsCreate

from src.core.models import Category, News, category_news_table
from src.core.schemas import CategoryNewsCreate


parsing_router = APIRouter(
    prefix="/parsing",
    tags=["Parsing"]
)


@parsing_router.get(
    path="/knife_media",
    description=f"Сбор данных с сайта knife.media"
)
async def add_news_to_db_from_media_info(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_auth)
):
    os.system(f"cd src/parser/parser/spiders/ "
              f"&& scrapy crawl knife_info_spider -O knife_media.json")
    with open("src/parser/parser/spiders/knife_media.json", 'r') as file:
        data = json.load(file)
    os.system("rm src/parser/parser/spiders/knife_media.json")

    all_cats_query = await session.execute(text("SELECT title FROM category"))
    all_categories = all_cats_query.scalars().all()

    all_titles_query = await session.execute(text("SELECT title FROM news"))
    all_titles = all_titles_query.scalars().all()

    for obj in data:
        if obj["title"] not in all_titles:
            for cat in obj["category_list"]:
                if cat not in all_categories:
                    try:
                        new_cat = CategoryCreate(title=cat)
                        stmt = insert(Category).values(**new_cat.model_dump())
                        await session.execute(stmt)
                        await session.commit()
                    except Exception:
                        raise HTTPException(
                            status_code=500,
                            detail="Ошибка добавления category"
                        )

            try:
                new_news = NewsCreate(
                    title=obj["title"],
                    text=obj["text"],
                    site_id=obj["site_id"],
                    url=obj["url"]
                )
                stmt = insert(News).values(**new_news.model_dump())
                await session.execute(stmt)
                await session.commit()
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка добавления news"
                )

            try:
                for cat in obj["category_list"]:
                    cat_id_query = await session.execute(text(f"SELECT id FROM category WHERE title = '{cat}'"))
                    category_id = cat_id_query.scalars().first()
                    print(category_id)
                    news_id_query = await session.execute(text(f"SELECT id FROM news WHERE title = '{obj['title']}'"))
                    news_id = news_id_query.scalars().first()
                    cat_news = CategoryNewsCreate(
                        category_id=category_id,
                        news_id=news_id
                    )
                    stmt = insert(category_news_table).values(**cat_news.model_dump())
                    await session.execute(stmt)
                    await session.commit()
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка добавления category_news"
                )

    return "Новости с сайта https://knife.media добавлены в Базу Данных"


@parsing_router.get(
    path="/naked_science",
    description="Сбор данных с сайта naked-science.ru"
)
async def add_news_to_db_from_naked_science(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_auth)
):
    os.system(f"cd src/parser/parser/spiders/ "
              f"&& scrapy crawl naked_science_spider -O naked_science.json")
    with open("src/parser/parser/spiders/naked_science.json", 'r') as file:
        data = json.load(file)
    os.system("rm src/parser/parser/spiders/naked_science.json")

    all_cats_query = await session.execute(text("SELECT title FROM category"))
    all_categories = all_cats_query.scalars().all()

    all_titles_query = await session.execute(text("SELECT title FROM news"))
    all_titles = all_titles_query.scalars().all()

    for obj in data:
        if obj["title"] not in all_titles:
            for cat in obj["category_list"]:
                if cat not in all_categories:
                    try:
                        new_cat = CategoryCreate(title=cat)
                        stmt = insert(Category).values(**new_cat.model_dump())
                        await session.execute(stmt)
                        await session.commit()
                    except Exception:
                        raise HTTPException(
                            status_code=500,
                            detail="Ошибка добавления category"
                        )

            try:
                new_news = NewsCreate(
                    title=obj["title"],
                    text=obj["text"],
                    site_id=obj["site_id"],
                    url=obj["url"],
                    views=obj["views"]
                )
                stmt = insert(News).values(**new_news.model_dump())
                await session.execute(stmt)
                await session.commit()
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка добавления news"
                )

            try:
                for cat in obj["category_list"]:
                    cat_id_query = await session.execute(text(f"SELECT id FROM category WHERE title = '{cat}'"))
                    category_id = cat_id_query.scalars().first()
                    print(category_id)
                    news_id_query = await session.execute(text(f"SELECT id FROM news WHERE title = '{obj['title']}'"))
                    news_id = news_id_query.scalars().first()
                    cat_news = CategoryNewsCreate(
                        category_id=category_id,
                        news_id=news_id
                    )
                    stmt = insert(category_news_table).values(**cat_news.model_dump())
                    await session.execute(stmt)
                    await session.commit()
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка добавления category_news"
                )

    return "Новости с сайта https://naked-science.ru добавлены в Базу Данных"
