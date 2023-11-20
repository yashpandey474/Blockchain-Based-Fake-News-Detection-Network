import streamlit as st
import change_screen
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *


def view_log_reputation():
    if st.session_state.screen == "view_log_reputation":
        # st.title("Log of Your Reputation Changes")
        st.markdown(
            "<h1 style='text-align: center;'>Log of Your Reputation Changes</h1>",
            unsafe_allow_html=True
        )
        log_reputation = st.session_state.p2pserver.accounts.accounts[
            st.session_state.p2pserver.wallet.get_public_key()
        ].reputation_changes
        
        table_data = []
        for reason, amount in log_reputation:
            table_data.append({
                    "Change Reason": reason,
                    "Change Amount": amount
                })

        st.dataframe(pd.DataFrame(table_data), height=500)

        if st.button("Back"):
            with st.spinner("Please Wait"): 
                change_screen.change_screen(st.session_state.previous_screen)

        
        
        
        
        
        
        