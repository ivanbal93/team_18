from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException

from fastapi_cache.decorator import cache

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from .models import Category, Site, News, Comment
from .schemas import NewsCreate, NewsUpdate, CommentCreate


def pagination_params(
    limit: int = 10,
    skip: int = 0
):
    return {"limit": limit, "skip": skip}


site_router = APIRouter(
    prefix="/site",
    tags=["Site"],
)


@site_router.get(
    path="/",
    description=f"Получение всех объектов класса Site. "
                f"Сортировка по названию."
)
async def get_all_sites(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Site).order_by(Site.title)
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


category_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@category_router.get(
    path="/",
    description=f"Получение всех объектов класса Category. "
                f"Сортировка по названию."
)
async def get_all_categories(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Category).order_by("title")
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


news_router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@news_router.get(
    path="/",
    description=f"Получение всех объектов класса News. "
                f"Сортировка по дате."
)
@cache(expire=30)
async def get_all_news(
    session: AsyncSession = Depends(get_async_session),
    pagination_params: dict = Depends(pagination_params)
):
    try:
        query = select(News).order_by(News.date)
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


@news_router.post(
    path="/",
    description=f"Добавление в БД объекта класса News. "
                f"Обязательные поля для заполнения: title, text, site_id. url"
)
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
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


@news_router.get(
    path="/favourites",
    description=f"Список объектов класса News, "
                f"добавленных в Избранное. Сортировка по дате."
)
async def get_favourite_news(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(News).where(News.is_favourite).order_by("date")
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(
            status_code=501,
            detail="Ошибка сервера"
        )


@news_router.get(
    path="/id/{news_id}",
    description=f"Получение объекта класса News по его id. "
                f"При отсутствии объекта возвращается 404."
)
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(News).where(News.id == news_id)
        result = await session.execute(query)
        result_final = result.scalars().one_or_none()
        if not result_final:
            raise NameError()
        return result_final

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="Новости с таким id не существует"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


# @news_router.patch(
#     path="/id/{news_id}",
#     description=f"Апдейт объекта класса News. "
#                 f"Обязательные поля для заполнения: title, text, is_favourite",
# )
# async def patch_news_by_id(
#     new: NewsUpdate,
#     news_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         query = select(News).where(News.id == news_id)
#         result = await session.execute(query)
#         print(result.scalars().first().__dict__)
#
#         stmt = update(News).values(**new.model_dump()).where(News.id == news_id)
#         await session.execute(stmt)
#         await session.commit()
#         return {"message": "Новость успешно обновлена!"}
#
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Ошибка сервера"
#         )


# @news_router.delete(
#     path="/id/{news_id}",
#     description="Удаление объекта класса News."
# )
# async def delete_news_by_id(
#     news_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         query = delete(News).where(News.id == news_id)
#         await session.execute(query)
#         await session.commit()
#         return {"message": "Новость успешно удалена!"}
#
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Ошибка сервера"
#         )


@news_router.get(
    path="/id/{news_id}/comments_list",
    description="Получение списка комментариев объекта News."
)
async def get_comments_by_news_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Comment).where(Comment.news_id == news_id)
        result = await session.execute(query)
        result_final = result.scalars().all()

        if not result_final:
            raise NameError()
        return result_final

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="У данной новости ещё нет комментариев администратора"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
    )


@news_router.post(
    path="/id/{news_id}/comments_list",
    description="Добавление комментария к объекту класса News."
)
async def add_comment(
    comment: CommentCreate,
    news_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        comment_dict = comment.model_dump()
        comment_dict["news_id"] = news_id
        stmt = insert(Comment).values(**comment_dict)
        await session.execute(stmt)
        await session.commit()
        return {"message": f"Комментарий успешно добавлен!"}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
    )


#здесь можно будет добавить в параметрах свойства юзера для определения наличия/отсуствия роли админа
# current_user = fastapi_users.current_user()
# @app.get("/protected_route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.login}"
