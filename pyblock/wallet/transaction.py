import time
from pyblock.chainutil import ChainUtil
from pyblock.ipfs.ipfs_handler import IPFSHandler
from pyblock.nlp.ml_model import *
from pyblock.wallet.wallet import Wallet
from typing import Type
    
class Transaction:
    def __init__(self):
        self.id = ChainUtil.id()
        self.ipfs_address = None
        self.sender_address = None
        self.sender_reputation = None
        self.model_score = None
        self.sign = None
        
    def get_transaction_score(self):
        content = IPFSHandler.get_from_ipfs(
            self.ipfs_address
        )

        return get_score(content)

    @staticmethod
    def generate_from_file(sender_wallet:Type[Wallet], file, blockchain):
        data = file.read()
        ipfs_address = IPFSHandler.put_to_ipfs(data)
        partial_transaction = Transaction()
        partial_transaction.ipfs_address = ipfs_address
        partial_transaction.sender_address = sender_wallet.public_key
        partial_transaction.sign = sender_wallet.sign(ChainUtil.hash(partial_transaction))
        partial_transaction.sender_reputation = blockchain.get_balance(sender_wallet.public_key)
        partial_transaction.model_score = partial_transaction.get_transaction_score()
        return partial_transaction

    @staticmethod
    def verify_partial_transaction(transaction, error_bound: float = 0.01):
        signature = transaction.sign
        transaction.sign = None
        transaction_hash = ChainUtil.hash(transaction)
        model_score = transaction.get_transaction_score()

        # Compare the model_score with transaction.model_score within the error bound
        if abs(model_score - transaction.model_score) > error_bound:
            return False
        
        return ChainUtil.verify_signature(
            transaction.sender_address,  # Public key
            signature,  # Signature to verify
            transaction_hash  # Hash of the content that was signed
        )

