# STREAMLIT GUI
import streamlit as st
import change_screen
from pyblock.wallet.transaction import *
from pyblock.blockchain.block import *
from pyblock.config import *
from datetime import datetime
import asyncio

def reader_navbar():
    return 


def main_page():
    user_type = st.session_state.user_type
    
    navigation_options = change_screen.navigation_options.get(st.session_state.user_type, ())
    selected_option = st.sidebar.radio("Navigation", navigation_options)
    if selected_option and change_screen.screen_mapping[selected_option] != st.session_state.screen:
        change_screen.change_screen_navbar(selected_option)
        
    welcome_message = f"Welcome, {st.session_state.name}!"

    st.markdown(f"## {welcome_message}")
    
    if user_type == "Auditor":
        st.markdown(change_screen.auditors_guidelines)
        
    else:
        st.markdown(change_screen.readers_guidelines)
        
        
    if st.button("Exit Application"):
        change_screen.change_screen("enter")
        
    
        