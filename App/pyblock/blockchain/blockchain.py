from .block import Block
from .account import *
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import *

secret = "i am the first leader"

TRANSACTION_TYPE = {
    "transaction": "TRANSACTION",
    "stake": "STAKE",
    "validator_fee": "VALIDATOR_FEE"
}


class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]
        self.accounts = Accounts()

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
        self.chain = new_chain

    def get_balance(self, public_key):
        return self.accounts.get_balance(public_key)
    
    def get_stake(self, public_key):
        return self.accounts.get_stake(public_key)

    def is_valid_block(self, block, transaction_pool, accounts):
        
        #IF ALL TRRANSACTIIONS EXISTS AND ALL ACCOUNTS HAVE THE BALANCE
        if not (transaction_pool.verify_transactions_exist(block.transactions)
        and accounts.verify_transactions_balance(block.transactions)):
            return False
        
        #IF PREVIOUS HASH IS CORRECT & CORRECT SIGNATURE & TRANSACTIONS
        if not (block.last_hash == self.chain[-1].hash and
            Block.verify_block(block)):
            return False
        
        return True
    
    def append_block(self, block, transaction_pool, accounts):
        #ALREADY CHECKED IF VALID WHEN BLOCK RECIEVED
        
        #UPDATE THE BALANCE OF SENDER
        accounts.update_accounts(block)
        
        #UPDATE THE TRANSACTION POOL
        transaction_pool.remove(block.transactions)
        
        #APPEND THE BLOCK TO CURRENT CHAIN
        self.chain.append(block)
        
        #BLOCK SUCCESSFULLY ADDED
        return True


