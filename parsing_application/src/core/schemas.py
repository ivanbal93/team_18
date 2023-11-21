from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    '''Класс пользователей'''

    id: int
    login: str
    password: str
    is_admin: bool
    news_id: int

    class Config:
        orm_model = True


class Site(BaseModel):
    '''Класс используемых сайтов'''

    id: str
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

    id: int
    title: str
    text: str
    is_favourite: bool
    date: datetime
    site_id: int
    url: str


class NewsCreate(News):
    pass

class NewsUpdate(News):
    pass


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