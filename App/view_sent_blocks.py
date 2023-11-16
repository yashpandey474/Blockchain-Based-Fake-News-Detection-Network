import streamlit as st
from change_screen import *
from pyblock.blockchain.block import *
import pandas as pd
from datetime import datetime

def view_sent_blocks():
    st.title("Blocks Broadcasted by you.")
    
    blocks = st.session_state.p2pserver.accounts.accounts[
        st.session_state.p2pserver.wallet.get_public_key()
    ].sent_blocks
    
    if len(blocks) == 0:
        st.write("You haven't broadcasted any blocks.")
    
    else:
        table_data = []
        for block in blocks:
            table_data.append({
                "Timestamp":  datetime.fromtimestamp(block.timestamp).strftime("%I:%M %p on %d %B, %Y"),
                "Number of Votes": len(block.votes),
                "Status": ("Yet to be verified" if block not in st.session_state.p2pserver.blockchain.chain else "Added to Chain")
            })
        
        st.dataframe(pd.DataFrame(table_data), height=500)
        
    if st.button("Back"):
        change_screen(st.session_state.previous_screen)
        
        
    
    
    
    