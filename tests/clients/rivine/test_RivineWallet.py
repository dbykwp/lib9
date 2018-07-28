"""
Test module for RivineWallet js9 client
"""

from js9 import j
import time
import json


from JumpScale9Lib.clients.blockchain.rivine.types.transaction import TransactionFactory
from JumpScale9Lib.clients.blockchain.rivine import utils
# txn = TransactionFactory.create_transaction(1)
# txn.add_data(bytearray('ot', encoding='utf-8'))
# txn.add_data(b'ot')
# txn.add_minerfee(100000000)
# print(txn.get_input_signature_hash(0).hex())
# raise RuntimeError('hello')


# use specific seed that has some funds
seed = 'siren own oil clean often undo castle sure creek squirrel group income size boost cart picture wing cram candy dutch congress actor taxi prosper'

client_data = {'bc_address': 'https://explorer.testnet.threefoldtoken.com/',
               'password_': 'test123',
               'minerfee': 100000000,
               'nr_keys_per_seed': 15,
               'seed_': seed}

rivine_client = j.clients.rivine.get('mytestwallet', data=client_data)
rivine_client.config.save()


bob_seed = 'easily comic language galaxy chalk near member project mind noodle height rice box famous before cancel traffic festival laugh exist trend ensure claw fish'
alice_seed = 'green industry hockey scrap below film stage fashion volcano quantum pilot sea fan reunion critic rack cover toy never warrior typical episode seed divide'

client_data['seed_'] = bob_seed
bob_wallet = j.clients.rivine.get('bobwallet', data=client_data).wallet


client_data['seed_'] = alice_seed
alice_wallet = j.clients.rivine.get('alicewallet', data=client_data).wallet



# create a wallet based on the generated Seed
wallet = rivine_client.wallet

assert len(wallet.addresses) == client_data['nr_keys_per_seed']

assert type(wallet._get_current_chain_height()) == int

address = '0145df536e9ad219fcfa9b2cd295d3499e59ced97e6cbed30d81373444db01acd563a402d9690c'
wallet._check_address(address=address)

#sync the wallet
assert type(wallet.current_balance) == float


def test_send_money_with_locktime():
    recipient = '01b1e730f6c8d8ef0615c05e87075265cf27b929a20767e3e652b6d303e95205bdd61fdfb88925'
    data = b"Hello from Cairo!"
    transaction = wallet.send_money(amount=2, recipient=recipient, data=data, locktime=time.time() + 500)
    assert transaction.id is not None
    return transaction

def test_send_to_many():
    unlockhashes = (bob_wallet.addresses[0], alice_wallet.addresses[0])
    multi_sig_txn = wallet.send_to_many(amount=5, recipients=unlockhashes, required_nr_of_signatures=2)
    assert multi_sig_txn.id is not None
    return multi_sig_txn



def test_load_transaction_from_json():
#     txn_json = """{"version": 1, "data": {"coininputs": [{"parentid": "5ff8302707e706d58cca5af07b22e80c1d9be7a72df5cb847ae8119d6572f69d", "ful
# fillment": {"type": 1, "data": {"publickey": "ed25519:c340e07e21c64faba56290260f076f544cb2901c75a209a9a8ea307fed537979", "signature":
# "7648792ae8961766933dc059539f6384a59cb7bcf5eea5f7bcc005e54fb236f3e438cbf308b92f379dc6da9686bf4bc993e38006acd865b4b12df2c4e803d902"}}}]
# , "coinoutputs": [{"value": "5000000000", "condition": {"type": 4, "data": {"unlockhashes": ["01c1f24eb0792086567fe9e2b8d6c2a66cca733b
# e2518fbac22ec8793da3b00b0759d37b6100bf", "016b0eb94e794ccfc596f0a181478f3ef9dfcc80046a2c33688ec3fa603ea67eb8643a7808e2ac"], "minimumsi
# gnaturecount": 2}}}, {"value": "304399999980", "condition": {"type": 1, "data": {"unlockhash": "012bdb563a4b3b630ddf32f1fde8d97466376a
# 67c0bc9a278c2fa8c8bd760d4dcb4b9564cdea6f"}}}], "minerfees": ["100000000"]}}"""

    txn_json = """{"version": 1, "data": {"coininputs": [{"parentid": "5ff8302707e706d58cca5af07b22e80c1d9be7a72df5cb847ae8119d6572f69d", "fulfillment": {"type": 1, "data": {"publickey": "ed25519:c340e07e21c64faba56290260f076f544cb2901c75a209a9a8ea307fed537979", "signature": "7648792ae8961766933dc059539f6384a59cb7bcf5eea5f7bcc005e54fb236f3e438cbf308b92f379dc6da9686bf4bc993e38006acd865b4b12df2c4e803d902"}}}], "coinoutputs": [{"value": "304399999980", "condition": {"type": 1, "data": {"unlockhash": "012bdb563a4b3b630ddf32f1fde8d97466376a67c0bc9a278c2fa8c8bd760d4dcb4b9564cdea6f"}}}], "minerfees": ["100000000"]}}"""

    txn = TransactionFactory.from_json(txn_json)
    # import pdb; pdb.set_trace()
    assert json.dumps(txn.json) == txn_json
    return txn

def test_create_multisig_wallet():
    # bob and alice are cosigners
    cosigners = [','.join(bob_wallet.addresses), ','.join(alice_wallet.addresses)]
    required_sig = 2
    multi_sig_client_data = {
        'multisig': True,
        'cosigners': cosigners,
        'required_sig': required_sig,
        'bc_address': client_data['bc_address'],
        'password_': client_data['password_'],
        'minerfee': client_data['minerfee']
    }

    multisig_wallet = j.clients.rivine.get('bob_and_alice_multisig_wallet', data=multi_sig_client_data).wallet
    # address = multisig_wallet.addresses[0]
    # address_info = wallet._check_address(address)
    # outputs = utils.collect_transaction_outputs(wallet._get_current_chain_height(), address=address, transactions=address_info['transactions'])
    # print(outputs)
    multisig_wallet._get_unspent_outputs()
    return multisig_wallet


import IPython
IPython.embed()
