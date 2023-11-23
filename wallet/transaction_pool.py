from typing import List
from .transaction import Transaction

# REPRESENTS THE MEMORY POOL [MEM-POOL OF TRANSACTIONS]


class TransactionPool:
    def __init__(self):
        # SET OF TRANSACTIONS
        self.transactions = set()

    def to_json(self):
        return [tx.to_json() for tx in self.transactions]

    @staticmethod
    def from_json(json_data):
        transactions = set([Transaction.from_json(tx) for tx in json_data])
        pool = TransactionPool()
        pool.transactions = transactions
        return pool

    def check_oldest_transaction(self, timestamp):
        # GET THE OLDEST TRANSACTION
        return False if len(self.transactions) == 0 else (min(self.transactions, key=lambda tx: tx.timestamp).timestamp <= timestamp)

    def add_transaction(self, transaction):
        # ADD A TRANSACTION TO SET
        return self.transactions.add(transaction)

    # REMOVE SOME TRANSACTIONS FROM SET
    def remove(self, transactions_to_remove: List[Transaction]):
        self.transactions = {tx for tx in self.transactions if tx.id not in {
            tx_to_remove.id for tx_to_remove in transactions_to_remove}}

        return True

    def transaction_exist(self, transaction):
        print(f"Checking transaction {transaction.id}")
        if transaction.id not in set(t.id for t in self.transactions):
            return False

        return True
    
    def verify_transactions_exist(self, transactions):
        print(f"VERIFYING TRANSACTIONS")
        # VERIFY ALL THE TRANSACTIONS EXIST & ALL ARE VERIFIED
        for transaction in transactions:
            # IF NOT IN MEMPOOL OR NOT VALID
            if not self.transaction_exist(transaction):
                return False

        return True
