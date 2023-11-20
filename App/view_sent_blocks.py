import streamlit as st
import change_screen as change_screen_
from pyblock.blockchain.block import *
import pandas as pd
from datetime import datetime

def view_sent_blocks():
    if st.session_state.screen == "view_sent_blocks":
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
            
        st.markdown(
            """
            # Blocks Broadcasted by You

            This page displays the blocks that you have broadcasted within the network.

            ## Block Broadcast Log:

            Below is a log containing the details of blocks you've broadcasted:

            """
        )
        
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
            st.markdown(
        """
        The table showcases each block's timestamp, the number of votes it received, and its current status within the network.
        """
    )
            
        # if st.button("Back"):
        #     with st.spinner("Please Wait"): 
        #         change_screen_.change_screen("main_page")
            
            
        
        
        
        