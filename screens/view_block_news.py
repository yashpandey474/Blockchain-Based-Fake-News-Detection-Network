#SHOW ALL NEWS ARTICLES ADDED TO BLOCKCHAIN
import streamlit as st
import change_screen as change_screen_
import pandas as pd
from datetime import datetime
from qr.transactions_info import show_transaction



def show_blocks_news():
    navigation_options = change_screen_.navigation_options.get(st.session_state.user_type, ())
    st.markdown(
            change_screen_.navbar_style, unsafe_allow_html=True)
    selected_option = st.sidebar.radio("\>> Navigation", navigation_options)
    if selected_option and change_screen_.screen_mapping[selected_option] != st.session_state.screen:
        change_screen_.change_screen_navbar(selected_option)
        
    if st.session_state.screen == "show_blocks":
        chain = st.session_state.p2pserver.blockchain.chain
        
        st.markdown(
            change_screen_.view_block_news_message,
            unsafe_allow_html=True
        )
        
        if len(chain) < 2:
            st.warning("The current ledger holds no news. Please return later")
        
        else:
            table_data = []
            
            for block in chain:
                for transaction in block.transactions:
                    
                    percent_fake_votes = 100*(len(transaction.negative_votes)/(len(transaction.negative_votes) + len(transaction.positive_votes)))
                    
                    table_data.append({
                        "Model Fake Score": transaction.model_score,
                        "Total Votes": len(transaction.positive_votes) + len(transaction.negative_votes),
                        "Percent of Fake Votes": str(percent_fake_votes) + "%",
                        "Percent of True Votes": str(100 - percent_fake_votes)  + "%",
                        "Content URL": "https://" + transaction.ipfs_address + ".ipfs.dweb.link",
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
            