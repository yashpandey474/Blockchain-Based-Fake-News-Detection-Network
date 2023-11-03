from ..chainutil import ChainUtil
# from .transaction import Transaction
# from .transaction_pool import TransactionPool

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyblock.blockchain.blockchain import Blockchain


class Wallet:
    def __init__(self):
        self.balance = 100
        self.key_pair, self.public_key = ChainUtil.gen_key_pair()

    def __str__(self):
        return f"Wallet -\n\tpublicKey: {self.public_key}\n\tbalance: {self.balance}"

    def sign(self, data_hash):
        return self.key_pair.sign(data_hash).to_hex()

    def get_balance(self, blockchain):
        return blockchain.get_balance(self.public_key)

    def get_public_key(self):
        return self.public_key
