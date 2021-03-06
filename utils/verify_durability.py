import asyncio
from tools.model import MyTool
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from actions import Action
from tools.crud import MyTools
from utils.next_action import next_action

action = Action()
mts = MyTools()


def verify_durability():
    mts.update()
    with Session(engine) as session:
        my_tools = session.scalars(select(MyTool)).all()
        for mt in my_tools:
            if mt.full_time is None:
                next_action()
            durability_need = (((mt.full_time - mt.next_availability) / 60 / 60) + 1) * mt.tools.durability_consumed
            if mt.current_durability < durability_need:
                print(f'{mt.asset_id} - {mt.tools.template_name} {mt.current_durability}/{mt.durability} restoring...')
                name = 'repair'
                data = {'asset_owner': mt.owner, 'asset_id': mt.asset_id}
                asyncio.get_event_loop().run_until_complete(action.claim(name, data))
                print('Ready to use tool!')
