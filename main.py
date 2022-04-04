

if __name__ == '__main__':
    from utils.api import Request
    c = Request('wax.eosrio.io', 'farmersworld')
    response = c.fetch(table='accounts', user='molivramento')
    print(response)
