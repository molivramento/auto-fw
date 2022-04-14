import asyncio
import datetime
import time
from users.crud import Users
from tools.crud import ToolConfs, MyTools
from mbs.crud import MbsConf, MyMbss
from utils.next_time import tool_next_time
from utils.verify_energy import verify_energy
from utils.verify_durability import verify_durability
from actions import Action
import schedule


users = Users()
toolconfs = ToolConfs()
my_tools = MyTools()
mbs = MbsConf()
my_mbs = MyMbss()
action = Action()


class Run:
    def start(self):
        users.create()
        toolconfs.create()
        my_tools.create()
        mbs.create()
        my_mbs.create()
        try:
            my_mbs.delete()
        except:
            pass
        Run.next_time(self)

    def next_time(self):
        verify_energy()
        verify_durability()
        data = tool_next_time()
        Run.schedule(self, data)

    def claim(self, d):
        if d['schema_name'] == 'mbs':
            name = 'mbsclaim'
        else:
            name = 'claim'
        data = {'owner': d['owner'], 'asset_id': d['asset_id']}
        act = action.claim(name, data)
        claim = asyncio.get_event_loop().run_until_complete(act)
        schedule.clear()
        if claim:
            verify_energy()
        Run.next_time(self)

    def schedule(self, data):
        nt = datetime.datetime.fromtimestamp(data['next_time']).strftime('%H:%M:%S')
        now = int(f'{time.time():.0f}')
        if data['next_time'] < now:
            nt = datetime.datetime.fromtimestamp(time.time() + 5).strftime('%H:%M:%S')
        schedule.every().day.at(nt).do(Run.claim, self, data)
        while True:
            schedule.run_pending()
            time.sleep(1)


r = Run()
r.start()

# next_availability = datetime.datetime.fromtimestamp(mt.next_availability).strftime('%H:%M:%S')
# print(f'{mt.asset_id} | {mt.tools.template_name} -> {next_availability}')
