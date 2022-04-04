from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Tool(Base):
    __tablename__ = 'tools'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, unique=True)
    template_name = Column(String)
    img = Column(String)
    schema_name = Column(String)
    type = Column(String)
    rarity = Column(String)
    level = Column(Integer)
    energy_consumed = Column(Integer)
    durability_consumed = Column(Integer)
    mints_gold = Column(Float)
    mints_wood = Column(Float)
    charged_time = Column(Integer)
    my_tools = relationship('MyTools')


class MyTools(Base):
    __tablename__ = 'my_tools'

    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey='tools.id')
    owner_id = Column(Integer, ForeignKey='users.id')
    asset_id = Column(Integer, unique=True)
    owner = Column(String)
    durability = Column(Integer)
    current_durability = Column(Integer, nullable=True)
    next_availability = Column(Integer, nullable=True)


if __name__ == '__main__':
    from utils.api import Request
    c = Request('wax.eosrio.io', 'farmersworld')
    response = c.fetch(table='toolconfs')
    print(response)
