from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
engine = create_engine('sqlite:///../database/database.db', future=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    account = Column(String, unique=True)
    energies = relationship('Energy')
    balances = relationship('Balance')


class Energy(Base):
    __tablename__ = 'energies'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    energy = Column(Integer)
    max_energy = Column(Integer)


class Balance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    wood = Column(Float)
    food = Column(Float)
    gold = Column(Float)


Base.metadata.create_all(engine)

if __name__ == '__main__':
    from utils.api import Request
    c = Request('wax.eosrio.io', 'farmersworld')
    response = c.fetch(table='accounts', user='molivramento')
    print(response)
