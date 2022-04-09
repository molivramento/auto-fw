from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction
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
        transaction = EosTransaction(
            ref_block_num=block['block_num'] & 65535,
            ref_block_prefix=block['ref_block_prefix'],
            actions=[action]
        )
        try:
            p = await rpc.sign_and_push_transaction(transaction, keys=[account.key])
            print(p)
            return True
        except Exception as e:
            print(e)
            return False
