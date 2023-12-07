from typing import Optional

from pydantic import BaseModel


class SiteCreate(BaseModel):
    title: str
    url: str
    is_active: bool = False

    class Config:
        orm_mode = True


class SiteUpdate(BaseModel):
    title: Optional[str]
    url: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
