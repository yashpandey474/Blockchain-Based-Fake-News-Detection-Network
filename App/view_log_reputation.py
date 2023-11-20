import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *


def view_log_reputation():
    if st.session_state.screen == "view_log_reputation":
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            """
            <style>
            .stRadio p{
                font-size: 20px;
            }
            .stRadio>label>div>p{
                font-size: 24px;
            }
            </style>
            """, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
        st.markdown(
    """
    # Log of Your Reputation Changes

    This page displays the log of your reputation changes within the network. Your reputation may change due to various reasons outlined below:

    ### Reasons for Reputation Changes:

    - **Initial Reputation Allocation**:
      Upon joining the network, users receive an initial reputation value. Auditors receive a notably higher reputation than readers, following successful authentication.

    - **Broadcasting News**:
      If the majority of auditors mark news as "Fake," the broadcaster faces a penalty proportionate to their balance. Conversely, if marked "True," the broadcaster receives a balance increase, but not proportionate to their existing balance to prevent disproportionate wealth accumulation.

    - **Block Validation**:
      Auditors that voted on a news post to be “Fake”/”True” and the majority voted for the opposite are penalized by a percentage of their stake in the network.

    - **Not Proposing a Block**:
      Block proposers that fail to utilize network time by creating a new block within the allotted time period are penalized on a percentage of their stake.

    ### Reputation Change Log:

    Below is a table displaying the details of your reputation changes:
    """
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



        
        
        
        
        
        
        