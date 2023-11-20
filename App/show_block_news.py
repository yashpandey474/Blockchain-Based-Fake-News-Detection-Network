#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from pyblock.qr.transactions_info import *



def show_blocks_news():
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
        
    if st.session_state.screen == "show_blocks":
        chain = st.session_state.p2pserver.blockchain.chain
        
        st.markdown(
            """
            ## View All Verified News

            Welcome to the 'View All Verified News' section.

            - Navigate through the sidebar options to explore.
            - This section presents details of all verified news available in the blockchain.
            - The table showcases various information:
              - Model Fake Score
              - Percentage of Fake and True Votes
              - Transaction and Block Creation Times
              - IPFS Address
              - Sender's Public Key
              - Validator's Public Key
              - Sender's Reputation
            - Click the 'QR Code' button to generate a QR code for each transaction.

            Dive in to explore the verified news available in the blockchain and stay informed!
            """,
            unsafe_allow_html=True
        )
        
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
                        "qr code": st.button(f"QR for {transaction.id}", on_click = show_transaction, kwargs={"transaction": transaction, "show":1})
                    })
            df = pd.DataFrame(table_data)

            st.dataframe(df, height=500)
            
