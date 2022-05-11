import asyncio
from users.model import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from actions import Action
from users.crud import Users

action = Action()
users = Users()


def verify_energy():
    with Session(engine) as session:
        users.update()
        user = session.scalars(select(User)).all()
        for u in user:
            print(u.max_energy)
            if u.energy <= u.max_energy * 0.2:
                print(f'Energy Status: {u.energy}')
                name = 'recover'
                recover_amount = u.max_energy - u.energy - 1
                data = {'owner': u.account, 'energy_recovered': recover_amount}
                asyncio.get_event_loop().run_until_complete(action.claim(name, data))
                print(f'New energy status: {u.max_energy}')
        session.commit()
