from ..chainutil import ChainUtil
from transaction import Transaction
from typing import Type
from transaction_pool import TransactionPool
from blockchain.blockchain import Blockchain

class Wallet:
    def __init__(self, secret):
        self.balance = 100
        self.key_pair,self.public_key = ChainUtil.gen_key_pair(secret)
    
    def __str__(self):
        return f"Wallet -\n\tpublicKey: {self.public_key}\n\tbalance: {self.balance}"

    def sign(self, data_hash):
        return self.key_pair.sign(data_hash).to_hex()

    def create_transaction(self, to, amount, txn_type, blockchain: Type[Blockchain], transaction_pool: Type[TransactionPool]):
        self.balance = self.get_balance(blockchain)
        if amount > self.balance:
            print(f"Amount: {amount} exceeds the current balance: {self.balance}")
            return
        transaction = Transaction.new_transaction(self, to, amount, txn_type)
        transaction_pool.add_transaction(transaction)
        return transaction

    def get_balance(self, blockchain: Type[Blockchain]):
        return blockchain.get_balance(self.public_key)

    def get_public_key(self):
        return self.public_key
