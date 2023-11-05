# Contains all regular block info, validation functions etc.

import hashlib
import json
# Assuming ChainUtil.py exists in the same directory
from pyblock.chainutil import ChainUtil
import time
from pyblock.wallet.transaction import Transaction
from typing import List  # Import Any if the actual type of signature is not known


class Block:
    def __init__(self, timestamp, lastHash, hash, transactions: List[Transaction], validator, signature):
        self.timestamp = timestamp
        self.lastHash = lastHash
        self.hash = hash
        self.transactions = transactions
        self.validator = validator
        self.signature = signature

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "lastHash": self.lastHash,
            "hash": self.hash,
            "transactions": [transaction.to_json() for transaction in self.transactions],
            "validator": self.validator,
            "signature": self.signature.hex() if self.signature else None
        }

    @staticmethod
    def genesis():
        return Block("genesis time", "----", "genesis-hash", [], None, None)

    @staticmethod
    def hash_transactions(transactions):
        # Create a new list of transactions with votes set to None
        transactions_for_hashing = [
            {**transaction.to_json(), "votes": None} for transaction in transactions
        ]
        # Hash the modified list of transactions
        return hashlib.sha256(json.dumps(transactions_for_hashing).encode('utf-8')).hexdigest()

    @staticmethod
    def create_block(last_block, data, wallet):
        timestamp = time.time()
        last_hash = last_block.hash
        # Create a deep copy of the data (which are transaction objects) for hashing
        transactions = [Transaction(**tx.to_json()) for tx in data]
        hash = Block.get_hash(timestamp, last_hash, transactions)
        validator = wallet.get_public_key()
        signature = Block.sign_block_hash(hash, wallet)
        return Block(timestamp, last_hash, hash, data, validator, signature)

    @staticmethod
    def get_hash(timestamp, last_hash, transactions):
        # Use the new helper method to hash transactions
        transactions_hash = Block.hash_transactions(transactions)
        sha = hashlib.sha256()
        sha.update(
            f"{timestamp}{last_hash}{transactions_hash}".encode('utf-8'))
        return sha.hexdigest()

    @staticmethod
    def block_hash(block):
        # Use the new helper method to hash transactions within the block
        return Block.get_hash(block.timestamp, block.last_hash, block.transactions)

    @staticmethod
    def sign_block_hash(hash, wallet):
        return wallet.sign(hash)

    @staticmethod
    def verify_block(block):
        # First, recreate the hash from the block's transactions and compare it to the stored hash
        recreated_hash = Block.block_hash(block)
        if block.hash != recreated_hash:
            return False  # The data has been tampered with if the hashes don't match

        # After confirming the hash matches, verify the signature to ensure it's from the validator
        return ChainUtil.verify_signature(
            block.validator,
            block.signature,
            recreated_hash  # Verify the signature against the recreated hash
        )
