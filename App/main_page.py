# STREAMLIT GUI
import streamlit as st
from change_screen import *
from pyblock.wallet.transaction import *
from pyblock.blockchain.block import *
from pyblock.config import *
from datetime import datetime
import asyncio

def main_page():
    st.write("Welcome, " + st.session_state.name)
    if st.session_state.screen == "main_page":
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
                
        if st.session_state.user_type == "Auditor":
            st.write("""As an auditor, you participate in out trusted private network. 
                     You must stake some "reputation" to become a validtor in the network. 
                     If you are chosen as a block proposing validator, you must choose some
                     transactions to include in a new block which is transmitted to other validators
                     and if  >=50\% of validators want the block to be included in the chain, it is added 
                     and you are rewarded with some reputation value. As a validator, you
                     would also (in addition to being in contention for becoming a block proposer) 
                     be able to vote on news in incoming blocks that other auditors chose to include 
                     as "Fake" or "True". A machine learning model is deployed that provides a
                     score from 0 to 1 as the probability of the news being fake according to our training data, this score
                     along with the reputation of the sender is available with every news received.
                     """) 
        
        # Map the nav_selection to corresponding actions
        if nav_selection == "Upload News":
            st.session_state.upload_file_executed = False
            with st.spinner("Please Wait"):
                change_screen("upload_file")
        elif nav_selection == "Verified News":
            with st.spinner("Please Wait"): 
                change_screen("show_blocks")
        elif nav_selection == "Account Info":
            with st.spinner("Please Wait"): 
                change_screen("account_info")
        elif nav_selection == "Sent News":
            with st.spinner("Please Wait"): 
                change_screen("view_sent_news")
        elif nav_selection == "Reputation Log":
            with st.spinner("Please Wait"): 
                change_screen("view_log_reputation")
        elif nav_selection == "Transactions in Mempool":
            with st.spinner("Please Wait"): 
                change_screen("show_transac")
        elif nav_selection == "Modify Stake" or nav_selection == "Become a Validator":
            st.session_state.stake_submitted = False
            with st.spinner("Please Wait"): 
                change_screen("become_validator")
        elif nav_selection == "Current Block Status":
            with st.spinner("Please Wait"): 
                change_screen("view_block_status")
        elif nav_selection == "Broadcasted Blocks":
            with st.spinner("Please Wait"): 
                change_screen("view_sent_blocks")
        elif nav_selection == "Enter Page":
            with st.spinner("Please Wait"): 
                change_screen("enter")

        #ADD A CLOCK OBJECT
        
        # await update_clock(t)
        # t = st.empty()
        # asyncio.run(update_clock(t))