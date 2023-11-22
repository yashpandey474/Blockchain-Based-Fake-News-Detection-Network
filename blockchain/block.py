# Contains all regular block info, validation functions etc.

import hashlib
import json
# Assuming ChainUtil.py exists in the same directory
from extra.chainutil import ChainUtil
import time
from wallet.transaction import Transaction
from typing import *
from wallet.wallet import Wallet
from extra.chainutil import *
import logging

# Setting up basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Block:
    def __init__(self, timestamp, last_hash, transactions: List[Transaction], validator, index: int, signature=None):
        """
        Initialize a new block in the blockchain.

        Parameters:
        - timestamp (float): The time at which the block was created.
        - last_hash (str): The hash of the previous block in the chain.
        - transactions (List[Transaction]): A list of transactions included in the block.
        - validator (str): The public key of the validator who created the block.
        - index (int): The index of the block in the blockchain.
        - signature (Optional[bytes]): The digital signature of the block, signed by the validator.

        Raises:
        - ValueError: If any of the parameters are invalid.
        """
        if not isinstance(timestamp, (int, float)):
            raise ValueError("Timestamp must be a number")
        if not isinstance(last_hash, str):
            raise ValueError("Last hash must be a string")
        if not all(isinstance(tx, Transaction) for tx in transactions):
            raise ValueError(
                "All transactions must be instances of Transaction")
        if not isinstance(validator, str):
            raise ValueError("Validator must be a string")
        if not isinstance(index, int):
            raise ValueError("Index must be an integer")

        self.timestamp = timestamp
        self.last_hash = last_hash
        self.transactions = transactions
        self.validator = validator
        self.signature = signature
        self.votes = set()
        self.index = index

        logging.info(f"Block {self.index} initialized.")

    # FUNCTION TO CONVERT BLOCK TO JSON
    def to_json(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "last_hash": self.last_hash,
            "transactions": [transaction.to_json() for transaction in self.transactions],
            "validator": self.validator,
            "signature": str(self.signature.hex()) if self.signature else "",
            "votes": list(self.votes),
        }

    @staticmethod
    def from_json(data_json):
        """
        Create a Block object from a JSON representation.

        Parameters:
        - data_json (dict): The JSON representation of the block.

        Returns:
        - Block: The Block object created from the JSON data.

        Raises:
        - ValueError: If the JSON data is invalid.
        """
        try:
            block = Block(
                index=data_json["index"],
                timestamp=data_json["timestamp"],
                last_hash=data_json["last_hash"],
                transactions=[Transaction.from_json(
                    tx_data) for tx_data in data_json["transactions"]],
                validator=data_json["validator"],
                signature=bytes.fromhex(
                    data_json["signature"]) if data_json["signature"] else None,
            )
            block.votes = set(data_json["votes"])

            return block
        except KeyError as e:
            logging.error(f"KeyError in from_json: {e}")
            raise ValueError("Invalid JSON data for Block") from e

    # CREATE THE INITIAL BLOCK

    @staticmethod
    def genesis():
        """
        Generate the genesis block for the blockchain.

        Returns:
        - Block: The genesis block.
        """
        return Block(
            timestamp=1700289379,
            last_hash="0000",
            transactions=[],
            validator="Creators",
            signature=None,
            index=1
        )

    @staticmethod
    def create_block(lastBlock, data, wallet, blockchain):
        """
        Create a new block in the blockchain.

        Parameters:
        - lastBlock (Block): The last block in the blockchain.
        - data (List[Transaction]): The list of transactions for the new block.
        - wallet (Wallet): The wallet of the validator.
        - blockchain (Blockchain): The blockchain to which this block will be added.

        Returns:
        - Block: The newly created block.

        Raises:
        - ValueError: If the input parameters are invalid.
        """
        try:
            timestamp = int(time.time())
            last_hash = Block.block_hash(lastBlock)
            validator = wallet.get_public_key()
            block = Block(timestamp, last_hash, data,
                          validator, len(blockchain.chain) + 1)
            block.transactions = data
            block.signature = Block.getBlockSignature(block, wallet)
            logging.info(f"Block {block.index} created.")
            return block
        except Exception as e:
            logging.error(f"Error in create_block: {e}")
            raise ValueError("Error in creating block") from e

    @staticmethod
    def getBlockSignature(block, wallet: Type[Wallet]):
        block_data = {
            "timestamp": block.timestamp,
            "last_hash": block.last_hash,
            "transactions": [transaction.sign for transaction in block.transactions],
            "validator": block.validator
        }

        # USE SIGN AND VERIFY SIGN OF CHAINUTIL TO MAINTAIN CONSISTENCY
        signature = ChainUtil.sign(
            private_key=wallet.get_private_key(),
            data=block_data
        )

        # RETURN THE CREATED BLOCK
        return signature
    # No pow nonce here

    @staticmethod
    def get_hash(timestamp, last_hash, transactions):
        data = {
            "timestamp": timestamp,
            "last_hash": last_hash,
            "transactions": [transaction.sign for transaction in transactions]
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
        return Block.get_hash(block.timestamp, block.last_hash, block.transactions)

    @staticmethod
    def verify_block(block):
        print("VERIFYING BLOCK " + str(block.index) + "...")
        block_data = {
            "timestamp": block.timestamp,
            "last_hash": block.last_hash,
            "transactions": [transaction.sign for transaction in block.transactions],
            "validator": block.validator
        }

        for transaction in block.transactions:
            if not Transaction.verify_transaction(transaction):
                return False

        # VERIFY THE SIGNATURE OF THE BLOCK
        return ChainUtil.verify_signature(
            block.validator,
            block.signature,
            block_data  # Verify the signature against the recreated hash
        )
