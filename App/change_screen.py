# CHANGE THE SCREEN OF GUI
import streamlit as st
from pyblock.config import *
import time
import asyncio

async def watch(test):
    while True:
        if st.session_state.screen_changed:
            break
        
        current_time = int(time.time())
        time_elapsed = current_time - START_TIME.timestamp()
        time_remaining = BLOCK_VALIDATOR_CHOOSE_INTERVAL - (time_elapsed % BLOCK_VALIDATOR_CHOOSE_INTERVAL)
        test.markdown(
            f"""
            <p class="time">
                Time Remaining in Current Block Proposing Period: {str(time_remaining)}
            </p>
            """, unsafe_allow_html=True)
        await asyncio.sleep(1)
        
def change_screen(input_string):
    if input_string == "enter":
        st.session_state.gen_key_pressed = False
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.initialise = False
        st.session_state.user_type = ""
    
    st.session_state.screen_changed = True
    st.session_state.previous_screen = st.session_state.screen
    st.session_state.screen = input_string
    st.rerun()
