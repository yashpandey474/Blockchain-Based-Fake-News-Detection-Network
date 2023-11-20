# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *


def show_transactions():
    if st.session_state.screen == "show_transac":
        # nav_selection = st.sidebar.selectbox("Navigation", change_screen_.navigation_options.get(st.session_state.user_type, ()))
        # if nav_selection and change_screen_.screen_mapping[nav_selection] != st.session_state.screen:
        #     change_screen_.change_screen_navbar(nav_selection)
        
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
            "<h1 style='text-align: center;'>Current Transactions in Mempool</h1>",
            unsafe_allow_html=True
        )
        transac_pool = st.session_state.p2pserver.transaction_pool.transactions
        
        if len(transac_pool) < 1:
            st.write("The network doesn't have any mempool transactions currently. Please come back later.")
        
        else:
            table_data = []
            for transaction in transac_pool:
                content = IPFSHandler.get_from_ipfs(transaction.ipfs_address)
                table_data.append({
                    "Model Score": transaction.model_score,
                    "Sender Reputation": transaction.sender_reputation,
                    "Sender Stake": st.session_state.p2pserver.blockchain.get_stake(transaction.sender_address),
                    "Transaction Fee": transaction.fee,
                    "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "Title": content.split("\n")[0],
                    "Text": " ".join(content.split("\n")[1: ]),
                    "Sender Address": transaction.sender_address,
                    "ID": transaction.id
                })

            st.dataframe(pd.DataFrame(table_data), height=500)

        # if st.button("Back"):
        #     with st.spinner("Please Wait"):
        #         change_screen_.change_screen("main_page")
