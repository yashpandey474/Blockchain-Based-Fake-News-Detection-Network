from pyblock.blockchain.account import Accounts
from pyblock.config import *
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

    def can_add_block(self, block):
        print("VOTES  = ", len(block.votes))
        print("PEERS = ", (self.p2pserver.accounts.get_count_of_validators()))

        return len(block.votes) >= (0.5 * self.p2pserver.accounts.get_count_of_validators())

    def run_forever(self):
        while True:
            current_time = int(time.time())
            time_elapsed = current_time - START_TIME.timestamp()
            sleep_time = BLOCK_VALIDATOR_CHOOSE_INTERVAL - (time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL)
            print("Sleeping for {} seconds".format(sleep_time))
            time.sleep(sleep_time)

            # IF THERE WAS A RECEIVED BLOCK FROM PREVIOUS BLOCK PROPOSERR
            if self.p2pserver.received_block:

                # IF THE BLOCK HAD VOTES FROM MAJORITY
                if self.can_add_block(self.p2pserver.received_block):
                    print("RECEIVED BLOCK ADDED TO CHAIN\n")
                    # ADD THE BLOCK TO THE BLOCKCHAIN
                    self.p2pserver.blockchain.append_block(
                        self.p2pserver.received_block,
                        self.p2pserver.transaction_pool,
                        self.p2pserver.accounts
                    )

                else:
                    # PUNISH THE BLOCK PROPOSER FOR NO BLOCK!
                    self.p2pserver.accounts[self.p2pserver.block_proposer].balance -= PENALTY_NO_BLOCK
                    print("RECIEVED BLOCK DID NOT GET ENOUGH VOTES\n")

            # CHOOSE THE BLOCK PROPOSER AT THE START TO NOT HAVE DELAY BECAUSE OF APPENDING
            self.p2pserver.block_proposer = self.p2pserver.accounts.choose_validator(
                current_time)

            # SET THE RECEIVED BLOCK TO NONE
            self.p2pserver.received_block = None

            # IF WAS ABLE TO CHOOSE A BLOCK PROPOSER
            if self.p2pserver.block_proposer:
                print("BLOCK PROPOSER CHOSEN!.\n")

            else:
                print("NO BLOCK PROPOSER CHOSEN.\n")
