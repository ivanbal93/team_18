from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from .models import User

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get("/")
async def get_all_users(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(User).order_by("id")
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")


@user_router.get("/id/{user_id}")
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
    except Exception:
        raise HTTPException(status_code=501, detail="Ошибка сервера")

    if result.scalar():
        return result.scalar()
    else:
        raise HTTPException(status_code=404, detail="id не существует")