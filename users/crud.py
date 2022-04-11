from api import Request
from users.model import User, Energy, Balance
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine

c = Request('wax.eosrio.io', 'farmersworld')


class Users:
    def __init__(self):
        self.response = c.fetch(table='accounts', user='molivramento')

    def create(self):
        response = c.fetch(table='accounts', user='molivramento')
        for r in self.response['rows']:
            with Session(engine) as session:
                balance = Users.balances(self)
                user = User(account=r['account'],
                            energies=[Energy(energy=r['energy'],
                                             max_energy=r['max_energy'])],
                            balances=[Balance(wood=balance.get('WOOD'),
                                              gold=balance.get('GOLD'),
                                              food=balance.get('FOOD'))])
                try:
                    session.add(user)
                    session.commit()
                except:
                    session.close()

    def update(self):
        response = c.fetch(table='accounts', user='molivramento')
        for r in response['rows']:
            with Session(engine) as session:
                balance = Users.balances(self)
                user = session.scalars(select(User)
                                       .where(User.account == r['account'])).one()
                energy_id = session.scalars(select(Energy)
                                            .where(Energy.user_id == user.id)).one()
                balance_id = session.scalars((select(Balance)
                                              .where(Balance.user_id == user.id))).one()
                energy_id.energy = r['energy']
                balance_id.wood = balance.get('WOOD')
                balance_id.gold = balance.get('GOLD')
                balance_id.food = balance.get('FOOD')
                session.commit()

    def balances(self):
        for r in self.response['rows']:
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