from typing import Optional

from pydantic import BaseModel


class SiteCreate(BaseModel):
    title: str
    url: str

    class Config:
        orm_mode = True


class SiteUpdate(BaseModel):
    title: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True