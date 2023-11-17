# STREAMLIT GUI
import streamlit as st
from change_screen import *
from pyblock.wallet.transaction import *
from pyblock.blockchain.block import *
from datetime import datetime


def main_page():
    # st.title("Fake News Detection System Utilizing Blockchain")
    st.write("Welcome, " + st.session_state.name)

    # Create a navigation bar
    if st.session_state.user_type == "Reader":
        nav_selection = st.sidebar.selectbox("Navigation",
                                            ("Main Page", "Upload News",
                                            "View Verified News",
                                            "View Account Info",
                                            "View Sent News",
                                            "View Reputation Log",
                                            "Enter Page"))
        
    if st.session_state.user_type == "Auditor":
        if st.session_state.validator:
            nav_selection = st.sidebar.selectbox("Navigation",
                                                 ("Main Page", "Upload News",
                                                  "Verified News",
                                                  "Account Info",
                                                  "Sent News",
                                                  "Reputation Log",
                                                  "Transactions in Mempool",
                                                  "Modify Stake",
                                                  "Current Block Status",
                                                  "Broadcasted Blocks",
                                                  "Enter Page"))
            
        else:
            nav_selection = st.sidebar.selectbox("Navigation",
                                                 ("Main Page", "Upload News",
                                                  "Verified News",
                                                  "Account Info",
                                                  "Sent News",
                                                  "Reputation Log",
                                                  "Transactions in Mempool",
                                                  "Become a Validator",
                                                  "Enter Page"))

    # Map the nav_selection to corresponding actions
    if nav_selection == "Upload News":
        st.session_state.upload_file_executed = False
        change_screen("upload_file")
    elif nav_selection == "Verified News":
        change_screen("show_blocks")
    elif nav_selection == "Account Info":
        change_screen("account_info")
    elif nav_selection == "Sent News":
        change_screen("view_sent_news")
    elif nav_selection == "Reputation Log":
        change_screen("view_log_reputation")
    elif nav_selection == "Transactions in Mempool":
        change_screen("show_transac")
    elif nav_selection == "Modify Stake" or nav_selection == "Become a Validator":
        st.session_state.stake_submitted = False
        change_screen("become_validator")
    elif nav_selection == "Current Block Status":
        change_screen("view_block_status")
    elif nav_selection == "Broadcasted Blocks":
        change_screen("view_sent_blocks")
    elif nav_selection == "Enter Page":
        change_screen("enter")

    # Rest of your code...
