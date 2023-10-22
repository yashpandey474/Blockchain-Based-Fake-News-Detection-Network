from .transaction import Transaction

TRANSACTION_THRESHOLD = 3  # Import or define your TRANSACTION_THRESHOLD here


class TransactionPool:
    def __init__(self):
        self.transactions = []

    def threshold_reached(self):
        return len(self.transactions) >= TRANSACTION_THRESHOLD

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        return len(self.transactions) >= TRANSACTION_THRESHOLD

    def valid_transactions(self):
        valid_txs = []
        for transaction in self.transactions:
            if not Transaction.verify_transaction(transaction):
                print(f"Invalid signature from {transaction.input['sender']}")
            else:
                valid_txs.append(transaction)
        return valid_txs

    def transaction_exists(self, transaction):
        return any(t.id == transaction.id for t in self.transactions)

    def clear(self):
        self.transactions = []
