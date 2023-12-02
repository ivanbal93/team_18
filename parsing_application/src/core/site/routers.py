from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.config import current_user_is_auth, current_user_is_admin
from src.authentication.models import User
from src.core.models import Site
from src.core.site.schemas import SiteUpdate, SiteCreate
from src.database import get_async_session

site_router = APIRouter(
    prefix="/site",
    tags=["Site"],
    # dependencies=[Depends(current_user_is_auth)]
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@site_router.post(
    path="/",
    description=f"Добавление в БД объекта класса Site. "
                f"Обязательные поля для заполнения: title, url"
)
async def add_site(
    new: SiteCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user_is_admin)
):
    try:
        stmt = insert(Site).values(**new.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"message": "Сайт успешно добавлен!"}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


@site_router.get(
    path="/id/{site_id}",
    description=f"Получение объекта класса Site по его id. "
                f"При отсутствии объекта возвращается 404."
)
async def get_site_by_id(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Site).where(Site.id == cat_id)
        result = await session.execute(query)
        result_final = result.scalars().one_or_none()
        if not result_final:
            raise NameError()
        return result_final

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="Сайта с таким id не существует"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@site_router.patch(
    path="/id/{site_id}",
    description=f"Апдейт объекта класса Site. "
                f"Обязательные поля для заполнения: is_active",
)
async def patch_site_by_id(
    new: SiteUpdate,
    cat_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user_is_admin)
):
    try:
        stmt = update(Site).values(**new.model_dump()).where(Site.id == cat_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Сайт успешно обновлен!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )


@site_router.delete(
    path="/id/{cat_id}",
    description="Удаление объекта класса Site."
)
async def delete_site_by_id(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user_is_admin)
):
    try:
        query = delete(Site).where(Site.id == cat_id)
        await session.execute(query)
        await session.commit()
        return {"message": "Сайт успешно удален!"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )