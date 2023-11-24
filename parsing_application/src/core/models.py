from datetime import datetime

from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, Column, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class Site(Base):
    '''Класс используемых сайтов'''

    __tablename__ = "site"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    news = relationship("News")


class Category(Base):
    '''Класс категорий новостей'''

    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    news = relationship("CategoryNews")


class News(Base):
    '''Класс новостей'''

    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    is_favourite = Column(Boolean, default=False, nullable=False)
    date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, index=True, autoincrement=True)
    url = Column(String, nullable=False)
    # likes = Column(Integer, nullable=True, default=0)
    # reposts = Column(Integer, nullable=True, default=0)
    site_id = Column(Integer, ForeignKey("site.id"))
    categories = relationship("CategoryNews")


class Comment(Base):
    '''Класс комментариев к новостям'''

    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow, index=True, autoincrement=True)
    news_id = Column(Integer, ForeignKey("news.id"))


class CategoryNews(Base):
    '''Промежуточный класс для связи M-t-M'''

    __tablename__ = 'category_news'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

