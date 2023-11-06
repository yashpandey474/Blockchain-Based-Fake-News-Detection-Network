#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
import streamlit as st
from change_screen import *
import pandas as pd

def show_blocks_news():
    
    
    chain = st.session_state.p2pserver.blockchain.chain
    
    
    if len(chain) < 2:
        st.write("The current ledger holds no news. Please return later")
    
    else:
        table_data = []
        
        for block in chain:
            for transaction in block.transactions:
                table_data.append({
                    "ID": transaction.id,
                    "Transaction Creation Time": transaction.timestamp,
                    "Block Creation Time": block.timestamp,
                    "IPFS Address": transaction.ipfs_address,
                    "Sender Address": transaction.sender_address,
                    "Validator Address": block.validator,
                    "Sender Reputation": transaction.sender_reputation,
                    "Sign of sender": transaction.sign,
                    "Model Score": transaction.model_score
                })
                
        st.dataframe(pd.DataFrame(table_data), height=500)
    
    if st.button("Back"):
        # Set the previous screen in the session state
        change_screen(st.session_state.previous_screen)