import time
from mbs.model import MyMbs
from mbs.crud import MyMbss
from tools.model import MyTool
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import engine
from actions import Action

action = Action()
my_mbs = MyMbss()


def mbs_amount(t):
    with Session(engine) as session:
        mbs = session.scalars(select(MyMbs)).all()
        saved_claims = 0
        for m in mbs:
            if m.mbs.type == t:
                saved_claims += m.mbs.saved_claims
        return saved_claims


def tool_next_time():
    with Session(engine) as session:
        data = []
        now = int(f'{time.time():.0f}')
        my_tools = session.scalars(select(MyTool)).all()
        my_mbs.update()
        mbs = session.scalars(select(MyMbs)).all()
        for m in mbs:
            if m.next_availability < now:
                data.append(
                    {
                        'next_time': m.next_availability,
                        'owner': m.owner,
                        'asset_id': m.asset_id,
                        'schema_name': 'mbs'
                    }
                )
        for mt in my_tools:
            saved_claims = mbs_amount(mt.tools.type)
            full_time = mt.next_availability + (saved_claims * mt.tools.charged_time)
            if full_time < now:
                data.append(
                    {
                        'next_time': mt.next_availability,
                        'owner': mt.owner,
                        'asset_id': mt.asset_id,
                        'schema_name': mt.tools.schema_name,
                        'template_name': mt.tools.template_name
                    }
                )
                print(f'Add {mt.tools.template_name} {mt.asset_id} {mt.owner}')
    return data
