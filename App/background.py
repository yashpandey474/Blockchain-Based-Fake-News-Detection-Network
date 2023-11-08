import threading
import time
import streamlit as st
from pyblock.peers import *
from pyblock.blockchain.account import *

def can_add_block(block):
    if block.votes >= (0.5 * len(PEERS)):
        return True
    
    return False

def background_task():
    while True:
        current_time = int(time.time())
        specific_time = config.START_TIME
        
        print(current_time - specific_time)
        if ((current_time - specific_time ) % 300 ) == 0:
            
            if "recieved_block" in st.session_state and st.session_state.received_block and can_add_block(st.session_state.received_block):
                st.session_state.p2pserver.blockchain.chain.append(st.session_state.received_block)
            
            st.session_state.receved_block = None
            st.session_state.block_proposer =  st.session_state.p2pserver.accounts.choose_validator()
            print("BLOCK PROPOSER CHOSEN: ", st.session_state.block_proposer)
            
        
        

