from utils.api import Request

c = Request('wax.eosrio.io', 'farmersworld')


def get_user():
    response = c.fetch(table='accounts', user='molivramento')
    print(response)


if __name__ == '__main__':
    get_user()
