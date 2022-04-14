from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


class Mbs(Base):
    __tablename__ = 'mbs'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, unique=True)
    name = Column(String)
    img = Column(String)
    type = Column(String)
    saved_claims = Column(Integer)
    additional_slots = Column(Integer)
    additional_energy = Column(Integer)
    lucky = Column(Integer)
    golds_mint = Column(Float)
    coins_mint = Column(Float)
    charged_time = Column(Integer)
    amount = Column(Integer)
    my_mbs = relationship('MyMbs', back_populates='mbs')


class MyMbs(Base):
    __tablename__ = 'my_mbs'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, unique=True)
    mbs_id = Column(Integer, ForeignKey('mbs.id'))
    owner = Column(String)
    unstaking_time = Column(Integer, nullable=True)
    next_availability = Column(Integer, nullable=True)

    mbs = relationship('Mbs', back_populates='my_mbs')


Base.metadata.create_all(engine)
