#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
import streamlit as st
import change_screen
import pandas as pd
from datetime import datetime
from pyblock.qr.transactions_info import *



def show_blocks_news():
    navigation_options = change_screen.navigation_options.get(st.session_state.user_type, ())
    selected_option = st.sidebar.radio("Navigation", navigation_options)
    if selected_option and change_screen.screen_mapping[selected_option] != st.session_state.screen:
        change_screen.change_screen_navbar(selected_option)
        
    if st.session_state.screen == "show_blocks":
        chain = st.session_state.p2pserver.blockchain.chain
        
        st.markdown(
            "<h1 style='text-align: center;'>View All Verified News</h1>",
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
                        "Sign of sender": transaction.sign,
                        "qr code": st.button(f"QR for {transaction.id}", on_click = show_transaction, kwargs={"transaction": transaction, "show":1})
                    })
            df = pd.DataFrame(table_data)

            st.dataframe(df, height=500)
            

        # if st.button("Back"):
        #     # Set the previous screen in the session state
        #     with st.spinner("Please Wait"): 
        #         change_screen.change_screen("main_page")