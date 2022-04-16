from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
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

    # energies = relationship('Energy', back_populates='owner_energies')
    # balances = relationship('Balance', back_populates='owner_balances')


# class Energy(Base):
#     __tablename__ = 'energies'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), unique=True)
#     energy = Column(Integer)
#     max_energy = Column(Integer)
#
#     owner_energies = relationship("User", back_populates="energies")
#
#
# class Balance(Base):
#     __tablename__ = 'balances'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     wood = Column(Float)
#     food = Column(Float)
#     gold = Column(Float)
#
#     owner_balances = relationship("User", back_populates="balances")


Base.metadata.create_all(engine)
