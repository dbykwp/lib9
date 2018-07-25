"""
Test module for RivineWallet js9 client
"""

from js9 import j
import time


from JumpScale9Lib.clients.blockchain.rivine.types.transaction import TransactionFactory
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

try:
    recipient = '01b1e730f6c8d8ef0615c05e87075265cf27b929a20767e3e652b6d303e95205bdd61fdfb88925'
    data = b"Hello from Cairo!"
    # transaction = wallet.send_money(amount=2, recipient=recipient, data=data, locktime=time.time() + 500)
    current_height = wallet._get_current_chain_height()
    # wallet.send_money(amount=2, recipient='01b1e730f6c8d8ef0615c05e87075265cf27b929a20767e3e652b6d303e95205bdd61fdfb88925', locktime=current_height + 5)
    # transaction = wallet._create_transaction(amount=1000000000, recipient=recipient, sign_transaction=True, custom_data=data)
    # transaction = wallet._create_transaction(amount=2000000000, recipient=recipient,minerfee=100000000, sign_transaction=True, custom_data=data, locktime=current_height + 5)

    # transaction = wallet.send_money(amount=2, recipient=recipient)
    # print(transaction.json)


    # create a multi-sig transaction
    unlockhashes = (bob_wallet.addresses[0], alice_wallet.addresses[0])
    multi_sig_txn = wallet.send_to_many(amount=5, recipients=unlockhashes, required_nr_of_signatures=2)
    print(multi_sig_txn.json)
finally:
    import IPython
    IPython.embed()
