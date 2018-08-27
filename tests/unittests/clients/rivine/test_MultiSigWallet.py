"""
Test module for MultiSigWallet module
"""

from JumpScale9Lib.clients.blockchain.rivine import RivineMultiSigWallet


def test_generate_multisig_addresses():
    """
    Tests generation of multisig addresses
    """

    cosigners = [['01c1f24eb0792086567fe9e2b8d6c2a66cca733be2518fbac22ec8793da3b00b0759d37b6100bf'], ['016b0eb94e794ccfc596f0a181478f3ef9dfcc80046a2c33688ec3fa603ea67eb8643a7808e2ac']]
    required_sig = 2

    multisig_wallet = RivineMultiSigWallet.RivineMultiSignatureWallet(cosigners=cosigners,
                                                                required_sig=required_sig,
                                                                bc_network="",
                                                                bc_network_password="")
    assert len(multisig_wallet.addresses) == 1
    assert multisig_wallet.addresses[0] == '032aa4d45db439b02d00e26990369281c83da55c111c3a4cc8c43e951324d3794bd62ed7d909b2'
