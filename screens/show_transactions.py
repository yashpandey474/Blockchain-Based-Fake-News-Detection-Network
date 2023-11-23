# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from ipfs.ipfs_handler import IPFSHandler


def show_transactions():
    if st.session_state.screen == "show_transac":
        # NAVIGATION BAR
        navigation_options = change_screen_.navigation_options.get(
            st.session_state.user_type, ())
        st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)

        selected_option = st.sidebar.radio(
            "\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)

        st.markdown(
            change_screen_.show_transactions_message,
            unsafe_allow_html=True
        )
        
        
        transac_pool = st.session_state.p2pserver.transaction_pool.transactions

        if len(transac_pool) < 1:
            st.warning(
                "The network doesn't have any mempool transactions currently. Please come back later.")

        else:
            table_data = []
            
            progress_bar = st.progress(0)
            current_progress = 1
            i = 1
            total_transactions = len(transac_pool)
            
            for transaction in transac_pool:
                table_data.append({
                    "Model Score": transaction.model_score,
                    "Sender Reputation": transaction.sender_reputation,
                    "Sender Stake": st.session_state.p2pserver.blockchain.get_stake(transaction.sender_address),
                    "Transaction Fee": transaction.fee,
                    "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "Content URL": "https://" + transaction.ipfs_address + ".ipfs.dweb.link",
                    "Sender Address": transaction.sender_address,
                    "ID": transaction.id
                })
                
                current_progress = int((i / total_transactions) * 100)
                progress_bar.progress(current_progress)
                i += 1

            progress_bar.empty()
            st.write("Transactions loaded successfully!")
            st.dataframe(pd.DataFrame(table_data), height=500)
