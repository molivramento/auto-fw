from mbs.model import MyMbs
from tools.model import MyTool
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from actions import Action
import time
from tools.crud import MyTools
import datetime

action = Action()
ms = MyTools()


def mbs_amount(t):
    with Session(engine) as session:
        my_mbs = session.scalars(select(MyMbs)).all()
        saved_claims = 0
        for m in my_mbs:
            if m.mbs.type == t:
                saved_claims += m.mbs.saved_claims
        session.commit()
        return saved_claims


def mbs_next_time(t):
    ...


def tool_next_time():
    with Session(engine) as session:
        ms.update()
        my_tools = session.scalars(select(MyTool)).all()
        next_time = int(f'{time.time():.0f}') + 90000
        asset_id = None
        owner = ''
        template_name = ''
        for mt in my_tools:
            mbs = mbs_amount(mt.tools.type)
            full_time = mt.next_availability + (mbs * mt.tools.charged_time)
            if full_time < next_time:
                next_time = full_time
                asset_id = mt.asset_id
                owner = mt.owner
                template_name = mt.tools.template_name
                session.commit()
        print(f'{asset_id} | {template_name} -> {datetime.datetime.fromtimestamp(next_time).strftime("%H:%M:%S")}')
        data = {'next_time': next_time, 'owner': owner, 'asset_id': asset_id}
        session.commit()
        return data
