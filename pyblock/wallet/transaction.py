import time
from pyblock.chainutil import ChainUtil
from pyblock.ipfs.ipfs_handler import IPFSHandler
from pyblock.nlp.ml_model import MLModel
from pyblock.wallet.wallet import Wallet
from typing import Type
class Transaction:
    def __init__(self):
        self.partialTransaction = None
        self.validator_address = None
        self.sign = None 
        self.votes= None
        self.timestamp = None
        self.model_score = None 

    @staticmethod
    def create_transaction(partial_transaction, validator_wallet:Type[Wallet]):
        # Verify the partial_transaction
        if not PartialTransaction.verify_partial_transaction(partial_transaction):
            print("Invalid PartialTransaction!")
            return None
        transaction = Transaction()
        transaction.partialTransaction = partial_transaction
        transaction.validator_address = validator_wallet.public_key
        transaction.timestamp = time.time()
        transaction.sign = validator_wallet.sign(ChainUtil.hash(partial_transaction))
        # Get the model score using MLModel and set it to the transaction
        transaction.model_score = MLModel.get_score(partial_transaction)
        return transaction
    
    @staticmethod
    def verify_transaction(transaction: Type[Transaction], error_bound: float = 0.01):
        signature = transaction.sign
        transaction_hash = ChainUtil.hash(transaction.partialTransaction)

        # Obtain the score from the ML model
        model_score = MLModel.get_score(transaction.partial_transaction)

        # Compare the model_score with transaction.model_score within the error bound
        if abs(model_score - transaction.model_score) > error_bound:
            return False

        return ChainUtil.verify_signature(
            transaction.validator_address,  # Public key
            signature,  # Signature to verify
            transaction_hash  # Hash of the content that was signed
        )
    
class PartialTransaction:
    def __init__(self):
        self.id = ChainUtil.id()
        self.ipfs_address = None
        self.sender_address = None
        self.sign = None
        self.timestamp = None

    @staticmethod
    def generate_from_file(sender_wallet:Type[Wallet], file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        ipfs_address = IPFSHandler.put_to_ipfs(data)
        partial_transaction = PartialTransaction()
        partial_transaction.ipfs_address = ipfs_address
        partial_transaction.sender_address = sender_wallet.public_key
        partial_transaction.timestamp = time.time()
        partial_transaction.sign = sender_wallet.sign(ChainUtil.hash(partial_transaction))
        return partial_transaction

    @staticmethod
    def verify_partial_transaction(partial_transaction):
        signature = partial_transaction.sign
        partial_transaction.sign = None
        transaction_hash = ChainUtil.hash(partial_transaction)
        return ChainUtil.verify_signature(
            partial_transaction.sender_address,  # Public key
            signature,  # Signature to verify
            transaction_hash  # Hash of the content that was signed
        )

