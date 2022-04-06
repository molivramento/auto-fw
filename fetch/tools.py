from utils.api import Request
from database.tool import Tool, MyTools, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

c = Request('wax.eosrio.io', 'farmersworld')


def get_toolconfs():
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
            tool = session.scalars(select(Tool).where(Tool.template_id == r['template_id'])).first()
            if tool is None:
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
                session.add(tool)
                session.commit()


def get_my_tools():
    response = c.fetch(table='tools', user='molivramento', index_position=2)
    with Session(engine) as session:
        for r in response['rows']:
            try:
                session.scalars(select(MyTools).where(MyTools.asset_id == r['asset_id'])).one()
                my_tool = session.scalars(select(MyTools).where(MyTools.template_id == r['template_id'])).one()
                my_tool.asset_id = r['asset_id']
                my_tool.owner = r['owner']
                my_tool.durability = r['durability']
                my_tool.current_durability = r['current_durability']
                my_tool.next_availability = r['next_availability']
                session.add(my_tool)
                session.commit()
            except:
                tool = session.scalars(select(Tool).where(Tool.template_id == r['template_id'])).one()
                my_tool = MyTools(tool_id=tool.id,
                                  asset_id=r['asset_id'],
                                  owner=r['owner'],
                                  durability=r['durability'],
                                  current_durability=r['current_durability'],
                                  next_availability=r['next_availability'],)
                session.add(my_tool)
                session.commit()


if __name__ == '__main__':
    get_toolconfs()
    get_my_tools()
