from pyblock.config import TRANSACTION_THRESHOLD
from typing import List
from .transaction import Transaction


class TransactionPool:
    def __init__(self):
        self.transactions = set()

    def add_transaction(self, transaction):
        return self.transactions.add(transaction)

    def valid_transactions(self):
        valid_txs = set()  # Change to a set
        for transaction in self.transactions:
            if not Transaction.verify_transaction(transaction):
                print(f"Invalid signature from {transaction.input['sender']}")
            else:
                valid_txs.add(transaction)  # Change to add to a set
        return valid_txs

    def remove(self, transactions_to_remove: List[Transaction]):
        self.transactions = {tx for tx in self.transactions if tx.id not in {
            tx_to_remove.id for tx_to_remove in transactions_to_remove}}

    def verify_transactions_exist(self, transactions):
        #VERIFY ALL THE TRANSACTIONS EXIST & ALL ARE VERIFIED
        for transaction in transactions:
            if transaction not in self.transactions or not Transaction.verify_transaction(transaction):
                return False
            
            
