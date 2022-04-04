
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Tools(Base):
    __tablename__ = 'tools'

    id = Column(Integer, primary_key=True)
    