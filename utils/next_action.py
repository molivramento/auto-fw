import time
from mbs.model import MyMbs
from tools.model import MyTool
from database import engine
from sqlalchemy import select
from sqlalchemy.orm import Session


def mbs_amount(t):
    with Session(engine) as session:
        mbs = session.scalars(select(MyMbs)).all()
        saved_claims = 0
        for m in mbs:
            if m.mbs.type == t:
                saved_claims += m.mbs.saved_claims
        return saved_claims


def next_action():
    with Session(engine) as session:
        my_tools = session.scalars(select(MyTool)).all()
        for mt in my_tools:
            saved_claims = mbs_amount(mt.tools.type)
            full_time = mt.next_availability + (saved_claims * mt.tools.charged_time)
            mt.full_time = full_time
            session.commit()
