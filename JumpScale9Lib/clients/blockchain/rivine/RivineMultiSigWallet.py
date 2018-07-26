"""
Module that defines required classes for Mulitsignature wallets
"""

from JumpScale9Lib.clients.blockchain.rivine.utils import hash as hash_func
from JumpScale9Lib.clients.blockchain.rivine.merkletree import Tree
from JumpScale9Lib.clients.blockchain.rivine.encoding import binary
from JumpScale9Lib.clients.blockchain.rivine.types.unlockhash import UnlockHash, UNLOCK_TYPE_MULTISIG

class RivineMultiSignatureWallet:
    """
    RivineMultiSignatureWallet class
    """

    def __init__(self, cosigners, required_sig, bc_network, bc_network_password, minerfee=100000000, client=None):
        """
        Initializes a new RivineMultiSignatureWallet

        @param cosigners: List of lists, the length of outer list indicates the number of cosigners and the length of the inner lists indicates the number of unlockhashes
        @param required_sig: Minimum number of signatures required for the output sent to any of the Multisig addresses to be spent
        @param bc_network: Blockchain network to use.
        @param bc_network_password: Password to send to the explorer node when posting requests.
        @param minerfee: Amount of hastings that should be minerfee (default to 0.1 TFT)
        @param client: Name of the insance of the j.clients.rivine that is used to create the wallet
        """
        self._cosigners = cosigners
        self._required_sig = required_sig
        self._bc_network = bc_network
        self._bc_network_password = bc_network_password
        self._minerfee = minerfee
        self._client = client
        self._nr_of_cosigners = len(self._cosigners)
        self._addresses = []



    @property
    def addresses(self):
        """
        Generates a list of multisig addresses
        """
        if not self._addresses and self._nr_of_cosigners > 0:
            for index in range(len(self._cosigners[0])):
                mtree = Tree(hash_func=hash_func)
                mtree.push(binary.encode(self._nr_of_cosigners))
                ulhs = []
                for sub_index in range(self._nr_of_cosigners):
                    ulhs.append(self._cosigners[sub_index][index])
                # make sure that regardless of the order of the unlockhashes, we sort them so that we always
                # produce the same multisig address
                for ulh in sorted(ulhs):
                    mtree.push(binary.encode(UnlockHash.from_string(ulh)))

                mtree.push(binary.encode(self._required_sig))
                address_hash = mtree.root()
                ulh = UnlockHash(unlock_type=UNLOCK_TYPE_MULTISIG, hash=address_hash)
                self._addresses.append(str(ulh))

        return self._addresses
