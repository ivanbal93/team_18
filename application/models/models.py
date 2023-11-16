from datetime import datetime

from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Column, Boolean

from application.database import Base


class User(Base):
    '''Класс пользователей'''

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


class Site(Base):
    '''Класс используемых сайтов'''

    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    url = Column(String)


class Cateogory(Base):
    '''Класс категорий новостей'''

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)


class News(Base):
    '''Класс новостей'''

    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    is_favourite = Column(Boolean, default=False, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))


class Comment(Base):
    '''Класс комментариев к новостям'''

    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    news_id = Column(Integer, ForeignKey("news.id"))


class CategoryNews(Base):
    '''Промежуточный класс для связи M-t-M'''

    __tablename__ = 'category_news'
    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))



