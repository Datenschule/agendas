#! -*- coding: utf-8 -*-

"""
Web Scraper Project
Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).
Database models part - defines table for storing scraped data.
Direct run will create the table.
"""

from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from .settings import DATABASE


DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return create_engine(URL(**DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Topic(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    detail = Column(String)
    number = Column(String)
    session = Column(Integer)
    description = Column(String)
    week = Column(String)
    year = Column(String)
    date = Column(String)
    duration = Column(Integer)

    # __table_args__ = (UniqueConstraint('period', 'session', 'number'),)

    def add_or_update(self, session):
        existing = session.query(Topic)\
                          .filter_by(title=self.title, session=self.session, week=self.week, year=self.year, detail = self.detail) \
                          .one_or_none()

        if existing:
            existing.number = self.number
            session.commit()

        else:
            session.add(self)
            session.commit()
