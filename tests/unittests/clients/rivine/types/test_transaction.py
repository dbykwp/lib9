"""
Unittests for module JumpScale9Lib.clients.blockchain.rivine.types.transaction
"""

import json
from unittest.mock import MagicMock

from JumpScale9Lib.clients.blockchain.rivine.types.transaction import DEFAULT_TRANSACTION_VERSION, TransactionFactory, TransactionV1, CoinInput, CoinOutput
from JumpScale9Lib.clients.blockchain.rivine.types.unlockconditions import UnlockHashCondition, LockTimeCondition, SingleSignatureFulfillment


def test_create_transaction_from_json():
    """
    Tests creating a transaction from a json string
    """
    txn_json = """{"version": 1, "data": {"coininputs": [{"parentid": "ae8d24095a01c7fc9a3cb0ba4720dc1b75acd73232abd1b9563ef0c26751f87d", "fulfillment": {"type": 3, "data": {"pairs": [{"publickey": "ed25519:1ad8c5878b594121b38652f2c2936f89d7dd66839b244cc3a14c05055efd358d", "signature": "c3347bf04a75588e9bbabd058eae2204c98bbc30ea8660036abd6924a6f4a78b57c6f7f39abc0db67c1826c9616c4abe4a353f9d87e66f5697931b2ce1844d04"}, {"publickey": "ed25519:903ef10891dea576512b76af4a90af86c71c7ec91095874862084683c3f236b3", "signature": "28275ef0579dd160839d73d9e8bc7ab41e53f1c6d255205ea78ce40753f7208d29eab888f74d759269c51f9404ea9b3f527ee3b86f2f1b49ba32fb3d82ebbd0c"}]}}}], "coinoutputs": [{"value": "1900000000", "condition": {"type": 1, "data": {"unlockhash": "0112a94261f6e4ef5bf0c8413b7bf318174810c9015fac8550b55d315061baccd2c464ae42baf0"}}}], "minerfees": ["100000000"]}}"""
    txn = TransactionFactory.from_json(txn_json)

    assert txn.json == json.loads(txn_json)

def test_create_transaction_v1():
    """
    Tests creating a V1 transaction
    """
    assert type(TransactionFactory.create_transaction(version=DEFAULT_TRANSACTION_VERSION)) == TransactionV1, "Wrong type transaction created"


def test_coininput_json(ed25519_key, ulh):
    """
    Tests the json output of CoinInput
    """
    expected_output = {'parentid': '01324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf57a828ea336a',
     'fulfillment': {'type': 1,
      'data': {'publickey': 'ed25519:6161616161616161616161616161616161616161616161616161616161616161',
       'signature': ''}}}
    ssf = SingleSignatureFulfillment(pub_key=ed25519_key)
    parent_id = str(ulh)
    ci = CoinInput(parent_id=parent_id, fulfillment=ssf)
    assert ci.json == expected_output


def test_coininput_sign(ed25519_key, ulh):
    """
    Tests siging a CoinInput
    """
    ssf = SingleSignatureFulfillment(pub_key=ed25519_key)
    ssf.sign = MagicMock()
    parent_id = str(ulh)
    ci = CoinInput(parent_id=parent_id, fulfillment=ssf)
    sig_ctx = {
        'input_idx': 0,
        'secret_key': None,
        'transaction': None,
    }
    ci.sign(input_idx=sig_ctx['input_idx'],
            transaction=sig_ctx['transaction'],
            secret_key=sig_ctx['secret_key'])
    assert ssf.sign.called_once_with(sig_ctx)


def test_coinoutput_binary(ulh):
    """
    Tests the binary output of a CoinOuput
    """
    expected_output = bytearray(b'\x02\x00\x00\x00\x00\x00\x00\x00\x01\xf4\x01!\x00\x00\x00\x00\x00\x00\x00\x012M\xcf\x02}\xd4\xa3\n\x93,D\x1f6Z%\xe8k\x17=\xef\xa4\xb8\xe5\x89H%4q\xb8\x1br\xcf')
    ulhc = UnlockHashCondition(unlockhash=ulh)
    co = CoinOutput(value=500, condition=ulhc)
    assert co.binary == expected_output

def test_coinoutput_json(ulh):
    """
    Tests the json output of a CoinOuput
    """
    expected_output = {'value': '500', 'condition': {'type': 1, 'data': {'unlockhash': '01324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf57a828ea336a'}}}
    ulhc = UnlockHashCondition(unlockhash=ulh)
    co = CoinOutput(value=500, condition=ulhc)
    assert co.json == expected_output


def test_transactionv1_json(recipient, ulh, spendable_key):
    """
    Tests the json output of the v1 transaction
    """
    expected_output = {'version': 1, 'data': {'coininputs': [{'parentid': '01324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf57a828ea336a', 'fulfillment': {'type': 1, 'data': {'publickey': 'ed25519:6161616161616161616161616161616161616161616161616161616161616161', 'signature': ''}}}], 'coinoutputs': [{'value': '500', 'condition': {'type': 1, 'data': {'unlockhash': '01479db781aae5ecbcc2331b7996b0d362ae7359b3fe25dcacdbf62926db506cbd3edf8bd46077'}}}], 'minerfees': ['100']}}
    txn = TransactionFactory.create_transaction(version=DEFAULT_TRANSACTION_VERSION)
    txn.add_coin_input(parent_id=str(ulh), pub_key=spendable_key.public_key)
    txn.add_coin_output(value=500, recipient=recipient)
    txn.add_minerfee(100)
    assert txn.json == expected_output


def test_transactionv1_get_input_signature_hash(recipient, ulh, spendable_key):
    """
    Tests generating signature hash of a transaction input
    """
    expected_output = b'#0@HW`X\x99c\x11\xf8\x08#\x15\x1a\x00\xe7e\xdb\xbf\x98e\xd1\xa7\xba\x94@\xd6\x1f\x1e\xc2/'
    txn = TransactionFactory.create_transaction(version=DEFAULT_TRANSACTION_VERSION)
    txn.add_coin_input(parent_id=str(ulh), pub_key=spendable_key.public_key)
    txn.add_coin_output(value=500, recipient=recipient)
    txn.add_minerfee(100)
    assert txn.get_input_signature_hash(0) == expected_output
