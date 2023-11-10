from pyblock.config import TRANSACTION_THRESHOLD
from typing import List
from .transaction import Transaction

#REPRESENTS THE MEMORY POOL [MEM-POOL OF TRANSACTIONS]
class TransactionPool:
    def __init__(self):
        #SET OF TRANSACTIONS
        self.transactions = set()

    def add_transaction(self, transaction):
        #ADD A TRANSACTION TO SET
        return self.transactions.add(transaction)

    #REMOVE SOME TRANSACTIONS FROM SET
    def remove(self, transactions_to_remove: List[Transaction]):
        self.transactions = {tx for tx in self.transactions if tx.id not in {
            tx_to_remove.id for tx_to_remove in transactions_to_remove}}
        
        return True
    def verify_transactions_exist(self, transactions):
        #VERIFY ALL THE TRANSACTIONS EXIST & ALL ARE VERIFIED
        for transaction in transactions:
            #IF NOT IN MEMPOOL OR NOT VALIDI
            if transaction not in self.transactions or not Transaction.verify_transaction(transaction):
                return False
            
            
