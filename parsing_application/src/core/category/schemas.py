from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    title: str
    is_active: bool = False

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    is_active: Optional[bool] = False

    class Config:
        orm_mode = True


