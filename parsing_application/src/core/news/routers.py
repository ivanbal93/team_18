from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .schemas import NewsUpdate, CommentCreate
from ..models import News, Comment
from ..utils import pagination_params
from ...authentication.config import current_user_is_admin, current_user_is_auth
from ...authentication.models import User

news_router = APIRouter(
    prefix="/news",
    tags=["News"],
    dependencies=[Depends(current_user_is_auth)]
)


@news_router.get(
    path="/",
    description=f"Получение всех объектов класса News. "
                f"Сортировка по дате."
)
# @cache(expire=60)
async def get_all_news(
    session: AsyncSession = Depends(get_async_session),
    pagination_params: dict = Depends(pagination_params)
):
    try:
        query = select(News).order_by(News.date)
        result = await session.execute(query)
        return result.scalars().all()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@news_router.patch(
    path="/id/{news_id}",
    description=f"Апдейт объекта класса News. "
                f"Обязательные поля для заполнения: title, text, is_favourite",
)
async def patch_news_by_id(
    new: NewsUpdate,
    news_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        stmt = update(News).values(**new.model_dump()).where(News.id == news_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Новость успешно обновлена!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@news_router.delete(
    path="/id/{news_id}",
    description="Удаление объекта класса News."
)
async def delete_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        query = delete(News).where(News.id == news_id)
        await session.execute(query)
        await session.commit()
        return {"message": "Новость успешно удалена!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )
