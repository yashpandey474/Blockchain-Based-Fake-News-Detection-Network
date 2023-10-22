# Contains all regular block info, validation functions etc.

import hashlib
import json
# Assuming ChainUtil.py exists in the same directory
from pyblock.chainutil import ChainUtil
import time


class Block:
    def __init__(self, timestamp, lastHash, hash, data, validator, signature):
        self.timestamp = timestamp
        self.lastHash = lastHash
        self.hash = hash
        self.data = data
        self.validator = validator
        self.signature = signature

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "lastHash": self.lastHash,
            "hash": self.hash,
            "data": self.data,
            "validator": self.validator,
            "signature": self.signature.hex() if self.signature else None
        }

    def __str__(self):
        return (f"Block -\n"
                f"Timestamp : {self.timestamp}\n"
                f"Last Hash : {self.lastHash}\n"
                f"Hash      : {self.hash}\n"
                f"Data      : {self.data}\n"
                f"Validator : {self.validator}\n"
                f"Signature : {self.signature}")

    @staticmethod
    def genesis():
        return Block("genesis time", "----", "genesis-hash", [], None, None)

    @staticmethod
    def create_block(lastBlock, _data, wallet):
        timestamp = time.time()
        lastHash = lastBlock.hash
        data = [_data]
        hash = Block.hash(timestamp, lastHash, data)
        validator = wallet.get_public_key()
        signature = Block.sign_block_hash(hash, wallet)
        return Block(timestamp, lastHash, hash, data, validator, signature)

    @staticmethod
    def getHash(timestamp, lastHash, data):
        sha = hashlib.sha256()
        sha.update(json.dumps(f"{timestamp}{lastHash}{data}").encode('utf-8'))
        return sha.hexdigest()

    @staticmethod
    def block_hash(block):
        return Block.getHash(block.timestamp, block.lastHash, block.data)

    @staticmethod
    def sign_block_hash(hash, wallet):
        return wallet.sign(hash)

    @staticmethod
    def verify_block(block):
        return ChainUtil.verify_signature(
            block.validator,
            block.signature,
            Block.block_hash(block)
        )

    @staticmethod
    def verify_leader(block, leader):
        return block.validator == leader
