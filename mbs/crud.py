from api import Request
from mbs.model import Mbs, MyMbs
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from utils.setup import api

c = Request(api, 'farmersworld')


def create_mbs_confs():
    response = c.fetch(table='mbsconf')
    with Session(engine) as session:
        for r in response['rows']:
            amount, resource = r['golds_mint'].split()
            mbs = Mbs(template_id=r['template_id'],
                      name=r['name'],
                      img=r['img'],
                      type=r['type'],
                      saved_claims=r['saved_claims'],
                      additional_slots=r['additional_slots'],
                      additional_energy=r['additional_energy'],
                      lucky=r['lucky'],
                      golds_mint=amount,
                      coins_mint=r['coins_mint'],
                      charged_time=r['charged_time'])
            try:
                session.add(mbs)
                session.commit()
            except:
                pass


def create_my_mbs():
    response = c.fetch(table='mbs', user='molivramento', index_position=2)
    for r in response['rows']:
        with Session(engine) as session:
            mbs = session.scalars(select(Mbs)
                                  .where(Mbs.template_id == r['template_id'])).one()
            my_mbs = MyMbs(mbs_id=mbs.id,
                           asset_id=r['asset_id'],
                           owner=r['owner'],
                           unstaking_time=r['unstaking_time'],
                           next_availability=r['next_availability'])
            try:
                session.add(my_mbs)
                session.commit()
            except:
                session.rollback()


def update_my_mbs():
    response = c.fetch(table='mbs', user='molivramento', index_position=2)
    for r in response['rows']:
        with Session(engine) as session:
            my_mbs = session.scalars(select(MyMbs)
                                     .where(MyMbs.asset_id == r['asset_id'])).one()
            my_mbs.unstaking_time = r['unstaking_time']
            my_mbs.next_availability = r['next_availability']
            session.commit()


def delete_my_mbs():
    response = c.fetch(table='mbs', user='molivramento', index_position=2)
    with Session(engine) as session:
        my_mbs = session.scalars(select(MyMbs)).all()
        mbs_db = set()
        current_mbs = set()
        for m in my_mbs:
            current_mbs.add(m.asset_id)

        for r in response['rows']:
            mbs_db.add(int(r['asset_id']))

        for rm in (current_mbs - mbs_db):
                rm_id = session.scalars(select(MyMbs).where(MyMbs.asset_id == rm)).first()
                session.delete(rm_id)
                session.commit()
