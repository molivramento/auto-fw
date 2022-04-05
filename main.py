import requests
import datetime
import time

d = datetime.datetime.timestamp(datetime.datetime.now())
print(d)

import requests

headers = {
    'authority': 'wax.api.aa.atomichub.io',
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://wax.atomichub.io',
    'referer': 'https://wax.atomichub.io/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
}

params = {
    'collection_name': 'farmersworld',
    'contract_whitelist': 'theonlykarma,sales.heroes,niftywizards,cc32dninenft',
    'limit': '40',
    'order': 'asc',
    'page': '1',
    'schema_name': 'tools',
    'seller_blacklist': 'dximg.wam,xpvrs.wam,5rrrc.wam,nnmnmnmnn.gm',
    'sort': 'price',
    'state': '1',
    'symbol': 'WAX',
}

response = requests.get('https://wax.api.aa.atomichub.io/atomicmarket/v2/sales', headers=headers, params=params)

print(response.json())
