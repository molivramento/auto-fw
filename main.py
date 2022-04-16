import time
import asyncio
import schedule
from actions import Action
from users.crud import Users
from mbs.crud import MbsConf, MyMbss
from tools.crud import ToolConfs, MyTools
from utils.next_time import tool_next_time
from utils.verify_energy import verify_energy
from utils.verify_durability import verify_durability

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
        Run.schedule(self)

    def next_time(self):
        verify_energy()
        verify_durability()
        return tool_next_time()

    def claim(self):
        next_time_items = Run.next_time(self)
        for nti in next_time_items:
            if nti['schema_name'] == 'mbs':
                name = 'mbsclaim'
            else:
                name = 'claim'
            data = {'owner': nti['owner'], 'asset_id': nti['asset_id']}
            act = action.claim(name, data)
            asyncio.get_event_loop().run_until_complete(act)

    def schedule(self):
        schedule.every(30).seconds.do(Run.claim, self)

        while True:
            schedule.run_pending()
            time.sleep(1)


r = Run()
r.start()

# next_availability = datetime.datetime.fromtimestamp(mt.next_availability).strftime('%H:%M:%S')
# print(f'{mt.asset_id} | {mt.tools.template_name} -> {next_availability}')
