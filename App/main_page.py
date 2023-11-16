# STREAMLIT GUI
import streamlit as st
from change_screen import *
from pyblock.wallet.transaction import *
from pyblock.blockchain.block import *

def main_page():
    # st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, " + st.session_state.name)

    c1,m,c2 = st.columns([0.4,0.6,0.4])

    with c1:

        if st.button("Upload New News"):
            # GET UPLOADED TEXT FILE
            st.session_state.upload_file_executed = False
            change_screen("upload_file")

        # VIEW NEWS STORED IN BLOCKCHAIN
        if st.button("View all Verified News"):
            change_screen("show_blocks")

        if st.button("View Account Information"):
            change_screen("account_info")

        if st.button("View Sent News/Transactions"):
            change_screen("view_sent_news")
        
        if st.button("View Log of Reputation Changes"):
            change_screen("view_log_reputation")
              
    with c2:
        if st.session_state.user_type == "Auditor":
            if st.button("View all transactions in mempool"):
                change_screen("show_transac")

            if not st.session_state.validator and st.button("Become a Validator"):
                st.session_state.stake_submitted = False
                change_screen("become_validator")
                
            if st.session_state.validator and st.button("Modify Your Stake in Network"):
                st.session_state.stake_submitted = False
                change_screen("become_validator")
                
            
        
        if (st.session_state.validator
        and st.button("View Current Block Status")):
            change_screen("view_block_status")
            
        if (st.session_state.validator
            and st.button("View Broadcasted Blocks")):
            change_screen("view_sent_blocks")

    st.write("")
    st.write("")
    
    
    if st.button("Exit Screen"):
        change_screen("enter")

    