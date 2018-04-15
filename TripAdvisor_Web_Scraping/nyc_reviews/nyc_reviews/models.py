from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_reviews_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Reviews(DeclarativeBase):
    """Sqlalchemy reviews model"""
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True)
    name = Column('name', String)
    title = Column('title', String, nullable=True)
    content = Column('content', String, nullable=True)
    recency = Column('recency', String, nullable=True)
    staysum = Column('staysum', String, nullable=True)
    stars = Column('stars', String, nullable=True)
    reviewer_loc = Column('reviewer_loc', String, nullable=True)
