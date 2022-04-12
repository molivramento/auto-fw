from mbs.model import MyMbs
from mbs.crud import MyMbss
from tools.model import MyTool
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import engine
from actions import Action
import datetime

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


def mbs_next_time():
    with Session(engine) as session:
        my_mbs.update()
        mbs_min = session.scalars(select(func.min(MyMbs.next_availability))).first()
        mbs = session.scalars(select(MyMbs)
                              .where(MyMbs.next_availability == mbs_min)).one()
        return mbs, mbs.mbs


def tool_next_time():
    with Session(engine) as session:
        m_mbs, mbs = mbs_next_time()
        my_tools = session.scalars(select(MyTool)).all()
        next_time = m_mbs.next_availability  # int(f'{time.time():.0f}') + 90000
        asset_id = m_mbs.asset_id
        owner = m_mbs.owner
        template_name = mbs.name
        schema_name = 'mbs'
        for mt in my_tools:
            mbs = mbs_amount(mt.tools.type)
            full_time = mt.next_availability + (mbs * mt.tools.charged_time)
            if full_time < next_time:
                next_time = full_time
                asset_id = mt.asset_id
                owner = mt.owner
                schema_name = mt.tools.schema_name
                template_name = mt.tools.template_name
        print(f'ASSET ID       -> {asset_id} \n'
              f'TEMPLATE NAME  -> {template_name} \n'
              f'TIME ACTION    -> {datetime.datetime.fromtimestamp(next_time).strftime("%H:%M:%S")}')
        data = {'next_time': next_time, 'owner': owner, 'asset_id': asset_id, 'schema_name': schema_name}
        return data
