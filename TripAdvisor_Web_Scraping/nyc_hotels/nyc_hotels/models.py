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

def create_hotels_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Hotels(DeclarativeBase):
    """Sqlalchemy hotels model"""
    __tablename__ = "hotels_v2"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    n_reviews = Column('n_reviews', String, nullable=True)
    st_addr = Column('st_addr', String, nullable=True)
    city = Column('city', String, nullable=True)
    state = Column('state', String, nullable=True)
    zip_cd = Column('zip_cd', String, nullable=True)
    excellent_ct = Column('excellent_ct', String, nullable=True)
    verygood_ct = Column('verygood_ct', String, nullable=True)
    average_ct = Column('average_ct', String, nullable=True)
    poor_ct = Column('poor_ct', String, nullable=True)
    terrible_ct = Column('terrible_ct', String, nullable=True)
    families = Column('families', String, nullable=True)
    couples = Column('couples', String, nullable=True)
    solo = Column('solo', String, nullable=True)
    business = Column('business', String, nullable=True)
    friends = Column('friends', String, nullable=True)
    #trav_types = Column('trav_types', String, nullable=True)
    spring = Column('spring', String, nullable=True)
    summer = Column('summer', String, nullable=True)
    fall = Column('fall', String, nullable=True)
    winter = Column('winter', String, nullable=True)
    #trav_time = Column('trav_time', String, nullable=True)
    rank = Column('rank', String, nullable=True)
    highlights = Column('highlights', String, nullable=True)
    prange = Column('prange', String, nullable=True)
    rooms = Column('rooms', String, nullable=True)
    hclass = Column('hclass', String, nullable=True)
    description = Column('description', String, nullable=True)
