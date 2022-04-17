from sqlalchemy import Column, Integer, String, Float
from database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    account = Column(String, unique=True)
    energy = Column(Integer)
    max_energy = Column(Integer)
    wood = Column(Float)
    food = Column(Float)
    gold = Column(Float)


Base.metadata.create_all(engine)
