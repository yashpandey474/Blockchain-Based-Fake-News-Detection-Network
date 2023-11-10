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
        self.positive_votes = None
        self.timestamp = int(time.time())
        self.fee = 0

    def to_json(self):
        return {
            "id": str(self.id),
            "ipfs_address": self.ipfs_address,
            "sender_address": self.sender_address,
            "sender_reputation": self.sender_reputation,
            "model_score": self.model_score,
            "sign": str(self.sign.hex()) if self.sign else "",
            "positive_votes": self.positive_votes,
            "timestamp": self.timestamp,
            "fee": self.fee
        }

    @staticmethod
    def from_json(json_data):
        transaction = Transaction()
        transaction.id = json_data["id"]
        transaction.ipfs_address = json_data["ipfs_address"]
        transaction.sender_address = json_data["sender_address"]
        transaction.sender_reputation = json_data["sender_reputation"]
        transaction.model_score = json_data["model_score"]
        transaction.fee = json_data["fee"]
    
        if "sign" in json_data and json_data["sign"]:
            transaction.sign = bytes.fromhex(json_data["sign"])
        else:
            transaction.sign = None
    
        transaction.timestamp = json_data["timestamp"]
        transaction.positive_votes = json_data["positive_votes"]
        
        return transaction
    
    
    def get_transaction_score(self):
        content = IPFSHandler.get_from_ipfs(
            self.ipfs_address
        )

        return get_score(content)

    @staticmethod
    def generate_from_file(sender_wallet: Type[Wallet], file, blockchain, fee):
        data = file.read()
        ipfs_address = IPFSHandler.put_to_ipfs(data)
        transaction = Transaction()
        transaction.timestamp = time.time
        transaction.ipfs_address = ipfs_address
        transaction.sender_address = sender_wallet.get_public_key()
        transaction.sign = sender_wallet.sign(ChainUtil.hash(transaction))
        transaction.sender_reputation = blockchain.get_balance(
            sender_wallet.get_public_key())
        transaction.model_score = transaction.get_transaction_score()
        transaction.timestamp = int(time.time())
        transaction.fee = fee
        return transaction

    @staticmethod
    def verify_transaction(transaction, error_bound: float = 0.01):
        signature = transaction.sign
        transaction.sign = None
        transaction_hash = ChainUtil.hash(transaction)
        model_score = transaction.get_transaction_score()
        transaction.sign = signature
        
        # Compare the model_score with transaction.model_score within the error bound
        if abs(model_score - transaction.model_score) > error_bound:
            return False

        return ChainUtil.verify_hashed_signature(
            transaction.sender_address,  # Public key
            signature,  # Signature to verify
            transaction_hash  # Hash of the content that was signed
        )
