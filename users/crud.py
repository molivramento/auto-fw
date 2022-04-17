from api import Request
from users.model import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from utils.setup import api, contract

c = Request(api, contract)


class Users:
    def create(self):
        with Session(engine) as session:
            response = c.fetch(table='accounts', user='molivramento')
            for r in response['rows']:
                try:
                    session.scalars(select(User).where(User.account == r['account'])).one()
                except:
                    balances = Users.balances(self, r['account'])
                    user = User(account=r['account'],
                                energy=r['energy'],
                                max_energy=r['max_energy'],
                                wood=balances.get('WOOD'),
                                gold=balances.get('GOLD'),
                                food=balances.get('FOOD'))
                    session.add(user)
                    session.commit()
                    print(f'{r["account"]} WOOD:{balances.get("WOOD")} GOLD:{balances.get("GOLD")} FOOD:{balances.get("FOOD")}')

    def update(self):
        with Session(engine) as session:
            user = session.scalars(select(User)).all()
            for u in user:
                response = c.fetch(table='accounts', user=u.account)
                balances = Users.balances(self, u.account)
                for r in response['rows']:
                    u.energy = r['energy']
                    u.wood = balances.get('WOOD')
                    u.food = balances.get('FOOD')
                    session.commit()

    def balances(self, user):
        response = c.fetch(table='accounts', user=user)
        for r in response['rows']:
            balance = {'WOOD': None, 'GOLD': None, 'FOOD': None}
            for b in r['balances']:
                amount, resource = b.split()
                if resource == 'WOOD':
                    balance['WOOD'] = amount
                elif resource == 'GOLD':
                    balance['GOLD'] = amount
                else:
                    balance['FOOD'] = amount
            return balance
