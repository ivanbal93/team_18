from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Site(BaseModel):
    '''Класс используемых сайтов'''

    title: str
    url: str

    class Config:
        orm_model = True


class Cateogory(BaseModel):
    '''Класс категорий новостей'''

    id: int
    title: str

    class Config:
        orm_model = True


class News(BaseModel):
    '''Класс новостей'''

    title: str
    text: str
    site_id: int
    url: str

    class Config:
        orm_model = True


class NewsCreate(News):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str]
    text: Optional[str]
    is_favourite: Optional[bool]


class Comment(BaseModel):
    '''Класс комментариев к новостям'''

    id: int
    title: str
    text: str
    date: str
    news_id: int


class CategoryNews(BaseModel):
    '''Промежуточный класс для связи M-t-M'''

    id: int
    news_id: int
    category_id: int