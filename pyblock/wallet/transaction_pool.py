from pyblock.config import TRANSACTION_THRESHOLD
from typing import List
from .transaction import Transaction


class TransactionPool:
    def __init__(self):
        self.transactions = set()

    def threshold_reached(self):
        return len(self.transactions) >= TRANSACTION_THRESHOLD

    def add_transaction(self, transaction):
        self.transactions.add(transaction)  # Set uses add instead of append
        return len(self.transactions) >= TRANSACTION_THRESHOLD

    def valid_transactions(self):
        valid_txs = set()  # Change to a set
        for transaction in self.transactions:
            if not Transaction.verify_transaction(transaction):
                print(f"Invalid signature from {transaction.input['sender']}")
            else:
                valid_txs.add(transaction)  # Change to add to a set
        return valid_txs

    def transaction_exists(self, transaction):
        return transaction in self.transactions  # Checking existence in a set

    def remove(self, transactions_to_remove: List[Transaction]):
        # Using set comprehension to remove transactions based on their ID
        self.transactions = {tx for tx in self.transactions if tx.id not in {
            tx_to_remove.id for tx_to_remove in transactions_to_remove}}

    def clear(self):
        self.transactions.clear()  # Clearing a set
