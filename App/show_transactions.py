# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
import streamlit as st
from change_screen import *
import pandas as pd
from datetime import datetime

def show_transactions():
    st.title("Current Network Transactions")
    transac_pool = st.session_state.p2pserver.transaction_pool.transactions
    
    if len(transac_pool) < 1:
        st.write("The network doesn't have any mempool transactions currently. Please come back later.")
    
    else:
        table_data = []
        for transaction in st.session_state.p2pserver.transaction_pool.transactions:
            table_data.append({
                "ID": transaction.id,
                "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                "IPFS Address": transaction.ipfs_address,
                "Sender Address": transaction.sender_address,
                "Sender Reputation": transaction.sender_reputation,
                "Sign": transaction.sign,
                "Model Score": transaction.model_score

            })

        st.dataframe(pd.DataFrame(table_data), height=500)

    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
