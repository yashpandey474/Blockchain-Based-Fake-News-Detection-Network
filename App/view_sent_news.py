import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *
def view_sent_news():
    if st.session_state.screen == "view_sent_news":
        navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
        st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
        selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
        if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
            change_screen_.change_screen_navbar(selected_option)
            
        st.markdown(
            change_screen_.view_sent_news_message,
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
                status_pool = st.session_state.p2pserver.transaction_pool.transaction_exist(transaction)
                transaction_data = {
                    "Status": ("Unconfirmed" if status_pool else "Added To Network Blockchain."),
                    "Model Score": transaction.model_score,
                    "Transaction Fee": transaction.fee,
                    "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "Title": content.split("\n")[0],
                    "Text": " ".join(content.split("\n")[1:]),
                    "ID": transaction.id
                }
                
                #ADD FIELDS FOR VOTES IF TRANSACTION HAS BEEN ADDED TO CHAIN
                if not status_pool:
                    percent_fake_votes = 100*(len(transaction.negative_votes)/(len(transaction.negative_votes) + len(transaction.positive_votes)))
                    transaction_data["Percent of Fake Votes"] = str(percent_fake_votes) + "%"
                    transaction_data["Percent of True Votes"] = str(100 - percent_fake_votes)  + "%"
                
                table_data.append(transaction_data)
                
                

            st.dataframe(pd.DataFrame(table_data), height=500)

        
        