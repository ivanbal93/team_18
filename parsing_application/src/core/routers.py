import os
import json

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.core.category.schemas import CategoryCreate
from src.core.news.schemas import NewsCreate

from .models import Category, News, category_news_table
from .schemas import CategoryNewsCreate


parsing_router = APIRouter(
    prefix="/parsing",
    tags=["Parsing"]
)


@parsing_router.post("/knife_parsing")
async def add_news_to_db_from_knife(
    session: AsyncSession = Depends(get_async_session)
):
    os.system(f"cd ~/team_18_back/parsing_application/src/parser/parser/spiders "
              f"&& scrapy crawl knife_spider -O "
              f"~/team_18_back/parsing_application/src/core/knife.json")
    with open("./src/core/knife.json", 'r') as file:
        data = json.load(file)
    os.system("rm ~/team_18_back/parsing_application/src/core/knife.json")

    all_cats_query = await session.execute(text("SELECT title FROM category"))
    all_categories = all_cats_query.scalars().all()

    all_titles_query = await session.execute(text("SELECT title FROM news"))
    all_titles = all_titles_query.scalars().all()

    for obj in data:
        if obj["title"] not in all_titles:
            for cat in obj["category_list"]:
                if cat.lower() not in all_categories:
                    try:
                        new_cat = CategoryCreate(title=cat.lower())
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

    return "Новости добавлены в Базу Данных"
