import streamlit as st
from change_screen import *
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *


def view_log_reputation():
    st.title("Log of Your Reputation Changes")
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
        change_screen(st.session_state.previous_screen)

    
    
    
     
    
    
    