# Contains all regular block info, validation functions etc.

import hashlib
import json
import numpy as np
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
        lastHash = Block.block_hash(lastBlock)
        #CONVERT THE TRANSACTIOONS TO JSON 
        transactions = [Transaction(**tx.to_json()) for tx in data]
        #GET THE VALIDATOR'S PUBLIC KEY
        validator = wallet.get_public_key()
        
        #SIGN THE BLOCK WITH VALIDATOR'S PRIVATE KEY
        block_data = {
            "timestamp": timestamp,
            "lastHash": lastHash,
            "transactions": [transaction.to_json() for transaction in transactions],
            "validator": validator
        }
        
        block_json = json.dumps(block_data)
        
        signature = wallet.sign(block_json)    
        
        #RETURN THE CREATED BLOCK
        return Block(
            timestamp = timestamp,
            lastBlock = lastBlock,
            transactions = data,
            validator = validator,
            signature = signature,
            index=  len(blockchain.chain) + 1)

    @staticmethod
    def get_hash(timestamp, lastHash, transactions):
        data = {
            "timestamp": timestamp,
            "last_hash": lastHash,
            "transactions": transactions
        }

        # Serialize the dictionary to a JSON string
        data_str = json.dumps(data, cls=CustomJSONEncoder)

        # Hash the serialized JSON string using SHA256
        sha = hashlib.sha256()
        sha.update(data_str.encode('utf-8'))

        return sha.hexdigest()

    @staticmethod
    def block_hash(block):
        # Use the new helper method to hash transactions within the block
        return Block.get_hash(block.timestamp, block.lastHash, block.transactions)


    @staticmethod
    def verify_block(block):
        #VERIFY ALL THE TRANSACTIONS IN BLOCK
        for transaction in block.transactions:
            if not Transaction.verify_transaction(transaction=transaction):
                return False
            

        block_data = {
            "timestamp": block.timestamp,
            "lastHash": block.lastHash,
            "transactions": [transaction.to_json() for transaction in block.transactions],
            "validator": block.validator
        }
        
        #VERIFY THE SIGNATURE OF THE BLOCK
        return ChainUtil.verify_signature(
            block.validator,
            block.signature,
            block_data  # Verify the signature against the recreated hash
        )


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.hex()
        elif isinstance(o, np.float32):
            return float(o)
        return json.JSONEncoder.default(self, o)
