from utils.api import Request
from database.user import User, Energy, Balance, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

c = Request('wax.eosrio.io', 'farmersworld')


def get_user():
    response = c.fetch(table='accounts', user='molivramento')
    with Session(engine) as session:
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
            try:
                user_id = session.scalars(select(User).where(User.account == r['account'])).one()
                user_id.energy = r['energy']
                user_id.wood = balance.get('WOOD')
                user_id.gold = balance.get('GOLD')
                user_id.food = balance.get('FOOD')
                session.commit()
            except:
                user = User(account=r['account'],
                            energies=[Energy(energy=r['energy'],
                                             max_energy=r['max_energy'])],
                            balances=[Balance(wood=balance.get('WOOD'),
                                              gold=balance.get('GOLD'),
                                              food=balance.get('FOOD'))])
                session.add(user)
                session.commit()


if __name__ == '__main__':
    get_user()
