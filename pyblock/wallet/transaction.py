import time
from ..chainutil import ChainUtil
from pyblock.ipfs.ipfs_handler import IPFSHandler

class Transaction:
    def __init__(self):
        self.partialTransaction = None
        self.validator_address = None
        self.sign = None 
        self.votes= None
        self.timestamp = None
        self.model_score = None 
        
import time
from ..chainutil import ChainUtil

class PartialTransaction:
    def __init__(self):
        self.id = ChainUtil.id()
        self.ipfs_address = None
        self.sender_address = None
        self.sign = None
        self.timestamp = None

    @staticmethod
    def generate_from_file(sender_wallet, file_path):
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

