import time
import asyncio
import datetime

from actions import Action

from database import engine

from users.crud import Users

from tools.model import MyTool
from tools.crud import ToolConfs, MyTools

from utils.next_action import next_action
from utils.verify_energy import verify_energy
from utils.verify_durability import verify_durability

from mbs.model import MyMbs
from mbs.crud import create_mbs_confs, create_my_mbs, delete_my_mbs, update_my_mbs

from sqlalchemy import select
from sqlalchemy.orm import Session


users = Users()
toolconfs = ToolConfs()
my_tools = MyTools()
action = Action()


class Run:
    def start(self):
        users.create()
        toolconfs.create()
        my_tools.create()
        create_mbs_confs()
        create_my_mbs()
        delete_my_mbs()
        Run.schedule(self)

    def next_time(self):
        update_my_mbs()
        verify_energy()
        verify_durability()
        next_action()

    def claim(self, next_time, name):
        data = {'owner': next_time.owner, 'asset_id': next_time.asset_id}
        act = action.claim(name, data)
        asyncio.get_event_loop().run_until_complete(act)

    def calc(self):
        with Session(engine) as session:
            next_mbs = session.scalars(select(MyMbs)).all()
            n_mbs = None
            next_tool = session.scalars(select(MyTool)).all()
            n_tool = None

            for nm in next_mbs:
                if n_mbs is None:
                    n_mbs = nm
                elif nm.next_availability < n_mbs.next_availability:
                    n_mbs = nm

            for nt in next_tool:
                if n_tool is None:
                    n_tool = nt
                elif nt.full_time < n_tool.full_time:
                    n_tool = nt

            if n_tool.full_time < n_mbs.next_availability:
                next_item = n_tool
                name = 'claim'
                next_time = n_tool.full_time
                template_name = n_tool.tools.template_name
                current_durability = n_tool.current_durability
                durability = n_tool.durability
            else:
                next_item = n_mbs
                name = 'mbsclaim'
                next_time = n_mbs.next_availability
                template_name = n_mbs.mbs.name
                current_durability = 0
                durability = 0
        t = datetime.datetime.fromtimestamp(next_time).strftime('%H:%M:%S')
        n = next_time - time.time()
        if n < 1:
            n = 1
        print(
            f'Next action: {t} - '
            f'{template_name} - '
            f'{next_item.asset_id} - '
            f'{current_durability}/'
            f'{durability}'
        )
        return {'t': t, 'next_time': next_time, 'name': name, 'next_item': next_item, 'n': n}

    def schedule(self):
        while True:
            Run.next_time(self)
            c = Run.calc(self)
            n = c['n']
            if n > time.time():
                n = 1
            time.sleep(n)
            Run.claim(self, c['next_item'], c['name'])


r = Run()
r.start()
# if __name__ == '--Main__':
#     r = Run()
#     r.start()
