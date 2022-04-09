from api import Request
from tools.model import Tool, MyTool
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine

c = Request('wax.eosrio.io', 'farmersworld')


class ToolConfs:
    def create(self):
        response = c.fetch(table='toolconfs')
        with Session(engine) as session:
            for r in response['rows']:
                mints = {'GOLD': None, 'WOOD': None}
                for m in r['mints']:
                    amount, resource = m.split()
                    if resource == 'GOLD':
                        mints['GOLD'] = amount
                    else:
                        mints['WOOD'] = amount
                tool = Tool(template_id=r['template_id'],
                            template_name=r['template_name'],
                            img=r['img'],
                            schema_name=r['schema_name'],
                            type=r['type'],
                            rarity=r['rarity'],
                            level=r['level'],
                            energy_consumed=r['energy_consumed'],
                            durability_consumed=r['durability_consumed'],
                            mints_gold=mints.get('GOLD'),
                            mints_wood=mints.get('WOOD'),
                            charged_time=r['charged_time'])
                try:
                    session.add(tool)
                    session.commit()
                except:
                    pass


class MyTools:
    def create(self):
        with Session(engine) as session:
            response = c.fetch(table='tools', user='molivramento', index_position=2)
            for r in response['rows']:
                tool = session.scalars(select(Tool)
                                       .where(Tool.template_id == r['template_id'])).one()
                my_tool = MyTool(tool_id=tool.id,
                                 asset_id=r['asset_id'],
                                 owner=r['owner'],
                                 durability=r['durability'],
                                 current_durability=r['current_durability'],
                                 next_availability=r['next_availability'])
                try:
                    session.add(my_tool)
                    session.commit()
                except:
                    session.rollback()

    def update(self):
        response = c.fetch(table='tools', user='molivramento', index_position=2)
        for r in response['rows']:
            with Session(engine) as session:
                my_tool = session.scalars(select(MyTool)
                                          .where(MyTool.asset_id == r['asset_id'])).one()
                my_tool.current_durability = r['current_durability']
                my_tool.next_availability = r['next_availability']
                session.commit()
