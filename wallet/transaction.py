import time
from extra.chainutil import ChainUtil
from ipfs.ipfs_handler import IPFSHandler
from nlp.ml_model import get_score
from wallet.wallet import Wallet
from typing import Type
from datetime import datetime


class Transaction:
    def __init__(self):
        self.id = str(ChainUtil.id())
        self.ipfs_address = None
        self.sender_address = None
        self.sender_reputation = None
        self.model_score = None
        self.sign = None
        self.positive_votes = set()
        self.negative_votes = set()
        self.timestamp = int(time.time())
        self.fee = 0

    def to_json(self):
        return {
            "id": str(self.id),
            "ipfs_address": self.ipfs_address,
            "sender_address": self.sender_address,
            "sender_reputation": self.sender_reputation,
            "model_score": self.model_score,
            "sign": self.sign.hex() if self.sign else "",
            "positive_votes": list(self.positive_votes),
            "negative_votes": list(self.negative_votes),
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
        transaction.timestamp = json_data["timestamp"]
        transaction.positive_votes = set(json_data["positive_votes"])
        transaction.negative_votes = set(json_data["negative_votes"])

        if "sign" in json_data and json_data["sign"]:
            transaction.sign = bytes.fromhex(json_data["sign"])
        else:
            transaction.sign = None

        return transaction

    def get_transaction_score(self):
        content = IPFSHandler.get_from_ipfs(
            self.ipfs_address
        )

        return get_score(content)

    @staticmethod
    def generate_from_file(sender_wallet: Type[Wallet], file, blockchain, fee):
        # GET DATA FROM FILE
        data = file.read()

        # INSTANTIATE TRANSACTION
        transaction = Transaction()

        # GET IPFS ADDRESS AFTER STORING CONTENT
        transaction.ipfs_address = IPFSHandler.put_to_ipfs(data)

        # SET CURRENT TIME
        transaction.timestamp = int(time.time())

        # SET SENDER PUBLIC KEY
        transaction.sender_address = sender_wallet.get_public_key()

        # SET SENDER REPUTATION
        transaction.sender_reputation = (blockchain.get_balance(sender_wallet.get_public_key())
                                         + blockchain.get_stake(sender_wallet.get_public_key()))

        # SET SCORE FROM ML MODEL
        transaction.model_score = transaction.get_transaction_score()

        # SET TRRANSACTION FEE
        transaction.fee = fee

        # SET SIGNATURE
        transaction_data = {
            "id": str(transaction.id),
            "ipfs_address": transaction.ipfs_address,
            "sender_address": transaction.sender_address,
            "sender_reputation": transaction.sender_reputation,
            "timestamp": transaction.timestamp,
            "fee": transaction.fee
        }

        private_key = sender_wallet.get_private_key()
        transaction.sign = ChainUtil.sign(
            private_key=private_key,
            data=transaction_data
        )

        return transaction

    @staticmethod
    def get_transaction_data(transaction):
        percent_fake_votes = 100*(len(transaction.negative_votes)/(
            len(transaction.negative_votes) + len(transaction.positive_votes)))

        return f"""
                         Model Fake Score": {transaction.model_score},
                        "Percent of Fake Votes": {str(percent_fake_votes) + "%"},
                        "Percent of True Votes": {str(100 - percent_fake_votes)  + "%"},
                        "Transaction Creation Time": {datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y")},
                        "Sender Reputation": {transaction.sender_reputation}
                """
    
    @staticmethod
    def verify_transaction(transaction, error_bound: float = 0.1):
        # HASH THE TRANSACTION WITH SIGNATURE AS NONE
        transaction_data = {
            "id": str(transaction.id),
            "ipfs_address": transaction.ipfs_address,
            "sender_address": transaction.sender_address,
            "sender_reputation": transaction.sender_reputation,
            "timestamp": transaction.timestamp,
            "fee": transaction.fee
        }

        # GET THE MODEL SCORE
        # model_score = transaction.get_transaction_score()
        # Ends up taking too much resources. not needed for proof of concept
        # # Compare the model_score with transaction.model_score within the error bound
        # if abs(model_score - transaction.model_score) > error_bound:
        #     print("MODEL SCORE NOT MATCHING")
        #     return False

        # VERIFY THE TRANSACTION SIGNATURE
        return ChainUtil.verify_signature(
            public_key=transaction.sender_address,  # Public key
            signature=transaction.sign,  # Signature to verify
            data=transaction_data  # Hash of the content that was signed
        )