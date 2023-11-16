#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
import streamlit as st
from change_screen import *
import pandas as pd
from datetime import datetime
from pyblock.qr.transactions_info import *



def show_blocks_news():
    chain = st.session_state.p2pserver.blockchain.chain
    
    st.title("View All Verified News.")
    
    if len(chain) < 2:
        st.write("The current ledger holds no news. Please return later")
    
    else:
        table_data = []
        
        for block in chain:
            for transaction in block.transactions:
                
                percent_fake_votes = 100*(len(transaction.negative_votes)/(len(transaction.negative_votes) + len(transaction.positive_votes)))
                
                table_data.append({
                    "Model Fake Score": transaction.model_score,
                    "Percent of Fake Votes": str(percent_fake_votes) + "%",
                    "Percent of True Votes": str(100 - percent_fake_votes)  + "%",
                    "ID": transaction.id,
                    "Transaction Creation Time": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "Block Creation Time": datetime.fromtimestamp(block.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                    "IPFS Address": transaction.ipfs_address,
                    "Sender Public Key": transaction.sender_address,
                    "Validator Public Key": block.validator,
                    # TODO: "Validator Reputation": st.session_state.accounts.get_
                    "Sender Reputation": transaction.sender_reputation,
                    "Sign of sender": transaction.sign,
                    "qr code": st.button(f"QR for {transaction.id}", on_click = show_transaction, kwargs={"transaction": transaction, "show":1})
                })
        df = pd.DataFrame(table_data)

        st.dataframe(df, height=500)
        

    if st.button("Back"):
        # Set the previous screen in the session state
        change_screen(st.session_state.previous_screen)