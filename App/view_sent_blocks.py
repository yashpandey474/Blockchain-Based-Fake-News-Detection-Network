import streamlit as st
import change_screen
from pyblock.blockchain.block import *
import pandas as pd
from datetime import datetime

def view_sent_blocks():
    if st.session_state.screen == "view_sent_blocks":
        # nav_selection = st.sidebar.selectbox("Navigation", change_screen.navigation_options.get(st.session_state.user_type, ()))
        # if nav_selection and change_screen.screen_mapping[nav_selection] != st.session_state.screen:
        #     change_screen.change_screen_navbar(nav_selection)
        # st.title("Blocks Broadcasted by you.")
        navigation_options = change_screen.navigation_options.get(st.session_state.user_type, ())
        selected_option = st.sidebar.radio("Navigation", navigation_options)
        if selected_option and change_screen.screen_mapping[selected_option] != st.session_state.screen:
            change_screen.change_screen_navbar(selected_option)
            
        st.markdown(
            "<h1 style='text-align: center;'>Blocks Broadcasted by you</h1>",
            unsafe_allow_html=True
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
            
        # if st.button("Back"):
        #     with st.spinner("Please Wait"): 
        #         change_screen.change_screen("main_page")
            
            
        
        
        
        