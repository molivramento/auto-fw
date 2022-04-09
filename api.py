import requests


class Request:
    def __init__(self, api, contract):
        self.api = api
        self.contract = contract

    def fetch(self, table, index_position=1, key_type='i64', user=''):
        headers = {'authority': f'{self.api}'}
        data = f'{{' \
               f'"json":true,' \
               f'"code":"{self.contract}",' \
               f'"scope":"{self.contract}",' \
               f'"table":"{table}",' \
               f'"lower_bound":"{user}",' \
               f'"upper_bound":"{user}",' \
               f'"index_position":{index_position},' \
               f'"key_type":"{key_type}",' \
               f'"limit":"100",' \
               f'"reverse":false,' \
               f'"show_payer":false' \
               f'}}'
        response = requests.post(f'https://{self.api}/v1/chain/get_table_rows', headers=headers, data=data)
        return response.json()


if __name__ == '__main__':
    c = Request('wax.eosrio.io', 'farmersworld')
    response = c.fetch(table='mbsconf')
    print(response)
