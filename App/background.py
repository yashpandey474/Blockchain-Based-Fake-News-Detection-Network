import threading
import time
import streamlit as st
from pyblock import config
from pyblock.blockchain.account import *


def background_task():
    while True:
        current_time = int(time.time())
        specific_time = config.START_TIME
        
        if ((current_time - specific_time ) % 300 ) == 0:
            st.session_state.block_proposer =  st.session_state.p2pserver.accounts.choose_validator()
            print("BLOCK PROPOSER CHOSEN: ", st.session_state.block_proposer)
            
        
        

