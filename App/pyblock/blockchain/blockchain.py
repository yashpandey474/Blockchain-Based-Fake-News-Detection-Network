from .block import Block
from .account import *
from pyblock.wallet.wallet import Wallet
from pyblock.wallet.transaction_pool import * 


#CLASS FOR THE NETWORK'S BLOCKCHAIN
class Blockchain:
    def __init__(self):
        #LIST OF BLOCKS
        self.chain = [Block.genesis()]
        #ACCOUNTS ASSOCIATED
        self.accounts = Accounts()

    #CHECK IF THE RECEIVED CHAIN IS VALID
    def is_valid_chain(self, chain):
        #COMMON GENSIS BLOCK
        if str(chain[0]) != str(Block.genesis()):
            return False

        #FOR EVERY OTHER BLOCK
        for i in range(1, len(chain)):
            #CURRENT BLOCK
            block = chain[i]
            #PREVIOUS BLOCK
            last_block = chain[i - 1]

            #VERIFY BLOCK AND PREVIOUS BLOCK HASH
            if not Block.verify_block(block) or not Block.block_hash(last_block) != block.lastHash:
                return False

        return True

    #REPLACE THE CHAIN WITH RECEIVED CHAIN
    def replace_chain(self, new_chain):
        #IF SMALLER CHAIN; NEVER REPLACE
        if len(new_chain) <= len(self.chain):
            print("Received chain is not longer than the current chain")
            return
        
        #CHECK IF CHAIN IS VALID
        elif not self.is_valid_chain(new_chain):
            print("Received chain is invalid")
            return

        print("Replacing the current chain with new chain")
        #REPLACE THE CHAIN
        self.chain = new_chain

    #GET ACCOUNT BALANCE FROM PUBLIC KEY
    def get_balance(self, public_key):
        return self.accounts.get_balance(public_key)
    
    #GET STAKED AMOUNT FROM PUBLIC KEY
    def get_stake(self, public_key):
        return self.accounts.get_stake(public_key)

    #VERIFY BLOCK IS VALID [WHEN RECEIVED! AS THEN THE SENDERS MUST HAVE ENOUGH BALANCE FOR TRANSACTIONS.]
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
    
    #MAKE CHANGES IN ACCOUNTS AND TRANSACTION POOL
    def append_block(self, block, transaction_pool, accounts):

        #UPDATE THE BALANCE OF SENDER
        accounts.update_accounts(block)
        
        #UPDATE THE TRANSACTION POOL
        transaction_pool.remove(block.transactions)
        
        #APPEND THE BLOCK TO CURRENT CHAIN
        self.chain.append(block)
        
        #BLOCK SUCCESSFULLY ADDED
        return True


