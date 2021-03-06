import datetime
import time
from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction, exceptions
import utils.setup as setup
from tools.crud import MyTools

mts = MyTools()


class Action:
    async def claim(self, name, data):
        account = EosAccount(setup.user, private_key=setup.private_key)
        rpc = EosJsonRpc('https://' + setup.api)
        block = await rpc.get_head_block()
        action = EosAction(
            account=setup.contract,
            name=name,
            authorization=[account.authorization(setup.contract)],
            data=data)
        try:
            transaction = EosTransaction(
                ref_block_num=block['block_num'] & 65535,
                ref_block_prefix=block['ref_block_prefix'],
                actions=[action]
            )
            try:
                p = await rpc.sign_and_push_transaction(transaction, keys=[account.key])
                if name == 'claim':
                    print(f"{datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')} - "
                          f"{p['processed']['action_traces'][0]['inline_traces'][1]['act']['data']['rewards']}")
                elif name == 'mbsclaim':
                    try:
                        print(f"{datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')} - "
                              f"{p['processed']['action_traces'][0]['inline_traces'][2]['act']['data']['amount']} "
                              f"{p['processed']['action_traces'][0]['inline_traces'][3]['act']['data']['bonus_rewards']}")
                    except Exception as e:
                        print(e)
                else:
                    pass
            except exceptions.EosRpcException as error:
                time.sleep(60)
                print(f'Error: {error}')
                await rpc.sign_and_push_transaction(transaction, keys=[account.key])
            except Exception as e:
                print(e)
                time.sleep(60)
        except Exception as e:
            print(e)
