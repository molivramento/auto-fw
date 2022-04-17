from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


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

    my_tools = relationship('MyTool', back_populates='tools')


class MyTool(Base):
    __tablename__ = 'my_tools'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, unique=True)
    tool_id = Column(Integer, ForeignKey('tools.id'))
    owner = Column(String)
    durability = Column(Integer)
    current_durability = Column(Integer, nullable=True)
    next_availability = Column(Integer, nullable=True)
    full_time = Column(Integer, nullable=True)

    tools = relationship('Tool', back_populates='my_tools')


Base.metadata.create_all(engine)
