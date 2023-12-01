from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Site
from src.database import get_async_session


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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e.args
        )
