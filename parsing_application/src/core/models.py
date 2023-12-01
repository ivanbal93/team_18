from datetime import datetime

import pytz
from sqlalchemy import String, Integer, ForeignKey, Column, Boolean, Text, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
current_time = datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y %H-%M")


category_news_table = Table(  # ассоциативная таблица M-t-M
    "category_news",
    Base.metadata,
    Column("category_id", ForeignKey("category.id", ondelete="CASCADE"), primary_key=True),
    Column("news_id", ForeignKey("news.id", ondelete="CASCADE"), primary_key=True)
)


class Site(Base):
    '''Класс используемых сайтов'''

    __tablename__ = "site"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    news_list = relationship(
        argument="News",
        backref="site",
        cascade="save-update, merge, delete",
        passive_deletes=True
    )


class Category(Base):
    '''Класс категорий новостей'''

    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=False, nullable=False)
    news_list = relationship(
        argument="News",
        secondary=category_news_table,
        back_populates="category_list",
        cascade="save-update, merge, delete",
        passive_deletes=True
    )


class News(Base):
    '''Класс новостей'''

    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    is_favourite = Column(Boolean, default=False, nullable=False)
    date = Column(String, default=current_time, autoincrement=True)
    url = Column(String, nullable=False)
    like = Column(Integer, nullable=True, default=0)
    repost = Column(Integer, nullable=True, default=0)
    views = Column(Integer, nullable=True, default=0)
    site_id = Column(Integer, ForeignKey("site.id", ondelete="CASCADE"))
    category_list = relationship(
        argument="Category",
        secondary=category_news_table,
        back_populates="news_list",
        lazy="subquery",
        cascade="save-update, merge, delete",
        passive_deletes=True
    )
    comments_list = relationship(
        argument="Comment",
        backref="news",
        cascade="save-update, merge, delete",
        lazy="subquery"
    )


class Comment(Base):
    '''Класс комментариев к новостям'''

    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    date = Column(String, default=current_time, autoincrement=True)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"))
