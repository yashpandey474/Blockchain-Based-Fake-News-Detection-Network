import streamlit as st
from change_screen import *
import pandas as pd
from datetime import datetime
from pyblock.ipfs.ipfs_handler import *
def view_sent_news():
    st.title("News/Transactions broadcasted by you.")
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
            table_data.append({
                "Model Score": transaction.model_score,
                "Transaction Fee": transaction.fee,
                # TODO: "Status": 
                "Timestamp": datetime.fromtimestamp(transaction.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                "Title": content.split("\n")[0],
                "Text": " ".join(content.split("\n")[1:]),
                # "Sender Address": transaction.sender_address,
                "ID": transaction.id
            })

        st.dataframe(pd.DataFrame(table_data), height=500)

    if st.button("Back"):
        change_screen(st.session_state.previous_screen)

    
    