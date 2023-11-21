from typing import List
from .transaction import Transaction

# REPRESENTS THE MEMORY POOL [MEM-POOL OF TRANSACTIONS]


class TransactionPool:
    def __init__(self):
        # SET OF TRANSACTIONS
        self.transactions = set()

    @staticmethod
    def to_json(self):
        return [tx.to_json() for tx in self.transactions]

    def check_oldest_transaction(self, timestamp):
        # GET THE OLDEST TRANSACTION
        return False if len(self.transactions) == 0 else (min(self.transactions, key=lambda tx: tx.timestamp).timestamp <= timestamp)

    @staticmethod
    def from_json(self, json_data):
        self.transactions = {Transaction.from_json(tx) for tx in json_data}

    def add_transaction(self, transaction):
        # ADD A TRANSACTION TO SET
        return self.transactions.add(transaction)

    # REMOVE SOME TRANSACTIONS FROM SET
    def remove(self, transactions_to_remove: List[Transaction]):
        self.transactions = {tx for tx in self.transactions if tx.id not in {
            tx_to_remove.id for tx_to_remove in transactions_to_remove}}

        return True

    def verify_transactions_exist(self, transactions):
        # VERIFY ALL THE TRANSACTIONS EXIST & ALL ARE VERIFIED
        for transaction in transactions:
            # IF NOT IN MEMPOOL OR NOT VALID
            if transaction.id not in set(t.id for t in self.transactions):
                print("TRANSACTION NOT IN SET")
                return False

            if not Transaction.verify_transaction(transaction):
                print("VERIFICATION OF TRANSACTION FAILED")
                return False

        return True
