import requests
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.category.schemas import CategoryUpdate
from src.core.models import Category
from src.database import get_async_session


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
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Category).order_by("title")
        result = await session.execute(query)
        return result.scalars().all()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@category_router.get(
    path="/id/{category_id}",
    description=f"Получение объекта класса Category по его id. "
                f"При отсутствии объекта возвращается 404."
)
async def get_cat_by_id(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Category).where(Category.id == cat_id)
        result = await session.execute(query)
        result_final = result.scalars().one_or_none()
        if not result_final:
            raise NameError()
        return result_final

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="Категории с таким id не существует"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@category_router.patch(
    path="/id/{category_id}",
    description=f"Апдейт объекта класса Category. "
                f"Обязательные поля для заполнения: is_active",
)
async def patch_cat_by_id(
    new: CategoryUpdate,
    cat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = update(Category).values(**new.model_dump()).where(Category.id == cat_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Категория успешно обновлена!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@category_router.delete(
    path="/id/{cat_id}",
    description="Удаление объекта класса Category."
)
async def delete_cat_by_id(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = delete(Category).where(Category.id == cat_id)
        await session.execute(query)
        await session.commit()
        return {"message": "Категория успешно удалена!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )
