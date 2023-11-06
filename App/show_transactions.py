# SHOW ALL CURRENT TRANSACTIONS IN MEMPOOL
import streamlit as st
from change_screen import *
import pandas as pd

def show_transactions(transaction_pool):
    st.title("Current Network Transactions")

    table_data = []
    for transaction in transaction_pool.transactions:
        table_data.append({
            "ID": transaction.id,
            "Timestamp": transaction.timestamp,
            "IPFS Address": transaction.ipfs_address,
            "Sender Address": transaction.sender_address,
            "Sender Reputation": transaction.validator_address,
            "Sign": transaction.sign,
            "Model Score": transaction.model_score
        })

    st.dataframe(pd.DataFrame(table_data), height=500)

    if st.button("Back"):
        # Set the previous screen in the session state
        change_screen(st.session_state.previous_screen)
