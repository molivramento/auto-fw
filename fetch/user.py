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
