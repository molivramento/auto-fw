import asyncio
from users.model import User, Energy
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.setup import user
from database import engine
from actions import Action
from users.crud import Users

action = Action()
users = Users()


def verify_energy():
    with Session(engine) as session:
        users.update()
        user_id = session.scalars(select(User)
                                  .where(User.account == user)).one()
        energy = session.scalars(select(Energy)
                                 .where(Energy.user_id == user_id.id)).one()
        if energy.energy < energy.max_energy * 0.2:
            print(F'Current energy: {energy.energy} recovering... \n new current energy: {energy.max_energy}')
            name = 'recover'
            recover_amount = energy.max_energy - energy.energy
            data = {'owner': user_id.account, 'energy_recovered': recover_amount}
            asyncio.get_event_loop().run_until_complete(action.claim(name, data))
