from pyblock.blockchain.account import Accounts
from pyblock.config import START_TIME, BLOCK_VALIDATOR_CHOOSE_INTERVAL
from pyblock.peers import PEERS
import time
import streamlit as st
from pyblock.peers import *
from pyblock.blockchain.account import *
from pyblock.blockchain.block import *


# Background task that periodically checks if a block can be added


class Background:
    def __init__(self, p2pserver):
        self.time = None
        self.p2pserver = p2pserver

    def can_add_block(block):
        return len(block.votes) >= (0.5 * len(PEERS))

    def run_forever(self):
        while True:
            current_time = int(time.time())
            time_elapsed = current_time - START_TIME.timestamp()
            sleep_time = BLOCK_VALIDATOR_CHOOSE_INTERVAL - (time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL)

            print("Sleeping for {} seconds".format(sleep_time))
            time.sleep(sleep_time)


            #CHOOSE THE BLOCK PROPOSER AT THE START TO NOT HAVE DELAY BECAUSE OF APPENDING
            self.p2pserver.block_proposer = self.p2pserver.accounts.choose_validator(
                current_time)
            
            #IF THERE WAS A RECEIVED BLOCK FROM PREVIOUS BLOCK PROPOSERR
            if self.p2pserver.received_block:
                
                #IF THE BLOCK HAD VOTES FROM MAJORITY
                if self.can_add_block(self.p2pserver.received_block):
                    #ADD THE BLOCK TO THE BLOCKCHAIN
                    self.p2pserver.blockchain.append_block(
                        self.p2pserver.received_block,
                        self.p2pserver.transaction_pool,
                        self.p2pserver.accounts
                    )

            #SET THE RECEIVED BLOCK TO NONE
            self.p2pserver.received_block = None
            

            # IF WAS ABLE TO CHOOSE A BLOCK PROPOSER
            if self.p2pserver.block_proposer:
                print("BLOCK PROPOSER CHOSEN: " + self.p2pserver.block_proposer)
            else:
                print("NO BLOCK PROPOSER CHOSEN.")
