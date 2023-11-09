from pyblock.blockchain.account import Accounts
from pyblock.config import START_TIME, BLOCK_VALIDATOR_CHOOSE_INTERVAL
from pyblock.peers import PEERS
import threading
import time
import streamlit as st
from pyblock.peers import *
from pyblock.blockchain.account import *


def can_add_block(block):
    return block.votes >= (0.5 * len(PEERS))

# Background task that periodically checks if a block can be added


def background_task():
    print("BACKGROUND TASK STARTED")
    while True:
        current_time = int(time.time())
        if ((current_time - START_TIME.timestamp()) % BLOCK_VALIDATOR_CHOOSE_INTERVAL) == 0:
            # TODO: change it to active accounts number
            active_accounts = st.session_state.p2pserver.connections
            if "received_block" in st.session_state and st.session_state.received_block:
                if can_add_block(st.session_state.received_block):
                    st.session_state.p2pserver.blockchain.append_block(
                        st.session_state.received_block, st.session_state.p2pserver.transaction_pool, st.session_state.p2pserver.accounts)
                else:
                    pass
                    # If the condition does not match, add it back to the mempool (no need, since it is already in the mempool  )
                st.session_state.received_block = None

            # Choose the new block proposer if the number of active accounts meets the threshold, else take lite
            if len(active_accounts) >= (0.5 * len(PEERS)):
                st.session_state.block_proposer = st.session_state.p2pserver.accounts.choose_validator()
                print("BLOCK PROPOSER CHOSEN: ",
                      st.session_state.block_proposer)

            else:
                print("NOT ENOUGH VALIDATORS")
                pass  # Take lite

            time.sleep(BLOCK_VALIDATOR_CHOOSE_INTERVAL -
                       ((current_time - START_TIME) % BLOCK_VALIDATOR_CHOOSE_INTERVAL))
