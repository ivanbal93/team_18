from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .config import current_user_is_admin

from .models import User
from .schemas import UserUpdate, UserCreate

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.get(
    path="/",
    description=f"Получение всех объектов класса User. "
                f"Сортировка по id.",
)
async def get_all_users(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        query = select(User).order_by("id")
        result = await session.execute(query)
        return result.scalars().all()

    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка сервера")


@user_router.get(
    path="/email/{user_email}",
    description=f"Получение объекта класса User по его email. "
                f"При отсутствии объекта возвращается 404."
)
async def get_user_by_email(
    user_email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        result_final = result.scalars().one_or_none()
        if not result_final:
            raise NameError()
        return result_final

    except NameError:
        raise HTTPException(
            status_code=404,
            detail="Пользователя с такой электронной почтой не существует"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


@user_router.patch(
    path="/email/{user_email}",
    description=f"Апдейт объекта класса User."
                f"Обязательные поля для заполнения: is_admin."

)
async def update_user_by_email(
    user_email: EmailStr,
    is_admin: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        stmt = update(User).where(User.email == user_email).values(is_admin.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"message": "Информация о пользователе успешно обновлена!"}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )


@user_router.delete(
    path="/email/{user_email}",
    description="Удаление объекта класса User."
)
async def delete_user_by_email(
    user_email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user_is_admin)
):
    try:
        query = delete(User).where(User.email == user_email)
        await session.execute(query)
        await session.commit()
        return {"message": f"Пользователь {user_email} успешно удалён!"}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        )
