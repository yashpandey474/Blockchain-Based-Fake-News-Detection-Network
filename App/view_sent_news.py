import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *
def view_sent_news():
    if st.session_state.screen == "view_sent_news":
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
            ## News Broadcasted by You

            Welcome to the 'News Broadcasted' section.

            - View the transactions you have broadcasted to the network.
            - Review the transaction details and their associated content.
            
            """,
            unsafe_allow_html=True
        )
        
        sent_transactions = st.session_state.p2pserver.accounts.get_sent_transactions(
            st.session_state.p2pserver.wallet.get_public_key()
        )

        if len(sent_transactions) < 1:
            st.write(
                "You haven't broadcasted any news in the network yet.")

        else:
            table_data = []
            for transaction in sent_transactions:
                content = IPFSHandler.get_from_ipfs(transaction.ipfs_address)
                status = st.session_state.p2pserver.transaction_pool.transaction_exist(transaction)
                table_data.append({
                    "Status": ("Unconfirmed" if status else "Added To Network Blockchain."),
                    "Model Score": transaction.model_score,
                    "Transaction Fee": transaction.fee,
                    "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "Title": content.split("\n")[0],
                    "Text": " ".join(content.split("\n")[1:]),
                    "ID": transaction.id
                })

            st.dataframe(pd.DataFrame(table_data), height=500)

        
        