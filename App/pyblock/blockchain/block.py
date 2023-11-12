# Contains all regular block info, validation functions etc.

import hashlib
import json
# Assuming ChainUtil.py exists in the same directory
from pyblock.chainutil import ChainUtil
import time
from pyblock.wallet.transaction import Transaction
from typing import List  # Import Any if the actual type of signature is not known


class Block:
    def __init__(self, timestamp, lastBlock, transactions: List[Transaction], validator, index: int, signature = None):
        #TIME OF BLOCK CREATION
        self.timestamp = timestamp
        #HASH OF PREVIOUS BLOCK
        
        #GENESIS BLOCK
        if index == 1:
            self.lastHash = "0000"
        else:
            self.lastHash = Block.block_hash(lastBlock)
            
        #LIST OF TRANSACTIONS
        self.transactions = transactions
        #VALIDATOR PUBLIC KEY
        self.validator = validator
        #SIGNATURE BY VALIDATOR
        self.signature = signature
        
        #SET OF VOTES GIVEN [INITIALISE WITH JUST VALIDATOR]
        self.votes = set()
        #INDEX OF BLOCK IN CHAIN 
        self.index = index
 

    #FUNCTION TO CONVERT BLOCK TO JSON
    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "lastHash": self.lastHash,
            "hash": self.hash,
            "transactions": [transaction.to_json() for transaction in self.transactions],
            "validator": self.validator,
            "signature": self.signature.hex() if self.signature else None,
            "countofvotes": len(self.votes)
        }

    #CREATE THE INITIAL BLOCK
    @staticmethod
    def genesis():
        return Block(timestamp = int(time.time()), 
                     lastBlock=None, 
                     transactions=[],
                     validator="Creators",
                     signature = None, 
                     index = 1)

    #HASH THE TRANSACTIONS IN BLOCK WITHOUT CONSIDERING THE VOTES
    @staticmethod
    def hash_transactions(transactions):
        # Create a new list of transactions with votes set to None
        transactions_for_hashing = [
            {**transaction.to_json(), "votes": None} for transaction in transactions
        ]
        
        # Hash the modified list of transactions
        return hashlib.sha256(json.dumps(transactions_for_hashing).encode('utf-8')).hexdigest()

    @staticmethod
    def create_block(lastBlock, data, wallet, blockchain):
        #SET THE TIMESTAMP
        timestamp = time.time()
        #SET PREVIOUS BLOCK'S HASH
        last_hash = Block.block_hash(lastBlock)
        #CONVERT THE TRANSACTIOONS TO JSON 
        transactions = [Transaction(**tx.to_json()) for tx in data]
        #GENERATE HASH FOR SIGNING
        data_hash = Block.get_hash(timestamp, last_hash, transactions)
        #GET THE VALIDATOR'S PUBLIC KEY
        validator = wallet.get_public_key()
        #SIGN THE BLOCK WITH VALIDATOR'S PRIVATE KEY
        signature = wallet.sign_hashed_data(data_hash)
        #RETURN THE CREATED BLOCK
        return Block(timestamp, last_hash, data, validator, signature, len(blockchain.chain) + 1)

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
    def verify_block(block):
        #VERIFY ALL THE TRANSACTIONS IN BLOCK
        for transaction in block.transactions:
            if not Transaction.verify_transaction(transaction=transaction):
                return False
        #VERIFY THE SIGNATURE OF THE BLOCK
        return ChainUtil.verify_hashed_signature(
            block.validator,
            block.signature,
            Block.block_hash(block)  # Verify the signature against the recreated hash
        )
