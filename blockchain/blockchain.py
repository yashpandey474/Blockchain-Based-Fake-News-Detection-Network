from block import Block
from stake import Stake
from account import Account
from validators import Validators
from wallet import Wallet

secret = "i am the first leader"

TRANSACTION_TYPE = {
    "transaction": "TRANSACTION",
    "stake": "STAKE",
    "validator_fee": "VALIDATOR_FEE"
}

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]
        self.stakes = Stake()
        self.accounts = Account()
        self.validators = Validators()

    def add_block(self, data):
        block = Block.create_block(self.chain[-1], data, Wallet(secret))
        self.chain.append(block)
        print("NEW BLOCK ADDED")
        return block

    def create_block(self, transactions, wallet):
        block = Block.create_block(self.chain[-1], transactions, wallet)
        return block

    def is_valid_chain(self, chain):
        if str(chain[0]) != str(Block.genesis()):
            return False

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]

            if block.last_hash != last_block.hash or block.hash != Block.block_hash(block):
                return False

        return True

    def replace_chain(self, new_chain):
        if len(new_chain) <= len(self.chain):
            print("Received chain is not longer than the current chain")
            return
        elif not self.is_valid_chain(new_chain):
            print("Received chain is invalid")
            return

        print("Replacing the current chain with new chain")
        self.reset_state()
        self.execute_chain(new_chain)
        self.chain = new_chain

    def get_balance(self, public_key):
        return self.accounts.get_balance(public_key)

#TODO: check this make this random func
    def get_leader(self):
        return self.stakes.get_max(self.validators.list)

    def initialize(self, address):
        self.accounts.initialize(address)
        self.stakes.initialize(address)

    def is_valid_block(self, block):
        last_block = self.chain[-1]
        if (block.last_hash == last_block.hash and 
            block.hash == Block.block_hash(block) and 
            Block.verify_block(block) and
            Block.verify_leader(block, self.get_leader())):
            print("block valid")
            self.add_block(block)
            self.execute_transactions(block)
            return True
        else:
            return False

#TODO: check
    def execute_transactions(self, block):
        for transaction in block.data:
            t_type = transaction.type
            if t_type == TRANSACTION_TYPE["transaction"]:
                self.accounts.update(transaction)
                self.accounts.transfer_fee(block, transaction)
            elif t_type == TRANSACTION_TYPE["stake"]:
                self.stakes.update(transaction)
                self.accounts.decrement(transaction.input.from_address, transaction.output.amount)
                self.accounts.transfer_fee(block, transaction)
            elif t_type == TRANSACTION_TYPE["validator_fee"]:
                print("VALIDATOR_FEE")
                if self.validators.update(transaction):
                    self.accounts.decrement(transaction.input.from_address, transaction.output.amount)
                    self.accounts.transfer_fee(block, transaction)

    def execute_chain(self, chain):
        for block in chain:
            self.execute_transactions(block)

    def reset_state(self):
        self.chain = [Block.genesis()]
        self.stakes = Stake()
        self.accounts = Account()
        self.validators = Validators()
