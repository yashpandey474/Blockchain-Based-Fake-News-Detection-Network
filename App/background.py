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
    def __init__(self):
        self.time = None
        self.received_block = None
        self.block_proposer = None
        
    def can_add_block(block):
        return block.votes >= (0.5 * len(PEERS))
    
    def run_forever(self):
        while True:
            current_time = int(time.time())
            if ((current_time - START_TIME.timestamp()) % BLOCK_VALIDATOR_CHOOSE_INTERVAL) == 0:
                if self.received_block:
                    if self.can_add_block(self.received_block):
                        st.session_state.p2pserver.blockchain.append_block(
                            st.session_state.received_block, st.session_state.p2pserver.transaction_pool, st.session_state.p2pserver.accounts)
                    self.received_block = None

                    self.block_proposer = st.session_state.p2pserver.accounts.choose_validator()
                    print("BLOCK PROPOSER CHOSEN: ", st.session_state.block_proposer)

                time.sleep(BLOCK_VALIDATOR_CHOOSE_INTERVAL -
                        ((current_time - START_TIME) % BLOCK_VALIDATOR_CHOOSE_INTERVAL))
