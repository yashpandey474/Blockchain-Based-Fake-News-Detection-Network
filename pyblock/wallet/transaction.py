import time
from ..chainutil import ChainUtil

TRANSACTION_FEE = 5 # Import or define your TRANSACTION_FEE here

class Transaction:
    def __init__(self):
        self.id = ChainUtil.id()
        self.type = None
        self.input = None
        self.output = None

    @staticmethod
    def new_transaction(sender_wallet, recipient, amount, tx_type):
        if amount + TRANSACTION_FEE > sender_wallet.balance:
            print(f"Amount: {amount} exceeds the balance")
            return None
        
        return Transaction.generate_transaction(sender_wallet, recipient, amount, tx_type)

    @staticmethod
    def generate_transaction(sender_wallet, recipient, amount, tx_type):
        transaction = Transaction()
        transaction.type = tx_type
        transaction.output = {
            'recipient': recipient,
            'amount': amount - TRANSACTION_FEE,
            'fee': TRANSACTION_FEE,
            'timestamp': time.time(),
        }
        Transaction.sign_transaction(transaction, sender_wallet)
        return transaction

    @staticmethod
    def sign_transaction(transaction, sender_wallet):
        transaction.input = {
            'sender': sender_wallet.public_key,
            'signature': sender_wallet.sign(ChainUtil.hash(transaction.output))
        }

    @staticmethod
    def verify_transaction(transaction):
        return ChainUtil.verify_signature(
            transaction.input['sender'],
            transaction.input['signature'],
            ChainUtil.hash(transaction.output)
        )
