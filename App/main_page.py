# STREAMLIT GUI
import streamlit as st
from change_screen import *
from pyblock.wallet.transaction import *
from pyblock import config
from pyblock.blockchain.block import *
import time

def main_page():
    # st.title("Fake News Detection System Utilising Blockchain")
    st.write("Welcome, " + st.session_state.name)

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
        
    if st.session_state.user_type == "Auditor":
        if st.button("View all transactions in mempool"):
            change_screen("show_transac")

        if not st.session_state.validator and st.button("Become a Validator"):
            change_screen("become_validator")
            
        if st.session_state.validator and st.button("Modify Your Stake in Network"):
            change_screen("become_validator")
    
    if (st.session_state.validator
    and st.button("View Current Block Status")):
        change_screen("view_block_status")

    
    if st.button("Exit Screen"):
        change_screen("enter")

    