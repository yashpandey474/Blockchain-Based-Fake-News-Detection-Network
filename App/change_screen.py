# CHANGE THE SCREEN OF GUI
import streamlit as st
from pyblock.config import *
from account_info import *
from become_validator import *
from vote_on_block import *
from upload_file import *
from view_sent_news import *
from sign_up import *
from view_block_status import *
from view_sent_blocks import *
from view_log_reputation import *
from login import *
from main_page import *
from show_block_news import *
from show_transactions import *
from enter import *
import time
import asyncio

screen_functions = {
    "enter": enter,
    "login": login,
    "main_page": main_page,
    "account_info": show_account_info,
    "show_transac": show_transactions,
    "show_blocks": show_blocks_news,
    "sign_up": sign_up,
    "sign_up_generate": sign_up_generate,
    "become_validator": become_validator,
    "vote_on_block": vote_on_block,
    "upload_file": upload_file,
    "view_sent_news": view_sent_news,
    "vote_on_block": vote_on_block,
    "view_block_status": view_block_status,
    "propose_block": propose_block,
    "view_sent_blocks": view_sent_blocks,
    "view_log_reputation": view_log_reputation
}

entered_pages = set([
    "main_page",
    "account_info",
    "show_transac"
    "show_blocks",
    "become_validator",
    "vote_on_block",
    "upload_file",
    "view_sent_news",
    "vote_on_block",
    "view_block_status",
    "propose_block",
    "view_sent_blocks",
    "view_log_reputation"
])


if "validator" not in st.session_state:
    st.session_state.validator = False
    
navigation_options = {
        "Reader": ("Main Page", "Upload News", "View Verified News", "View Account Info", "View Sent News", "View Reputation Log", "Enter Page"),
        "Auditor": (
            "Main Page", "Upload News", "Verified News", "Account Info", "Sent News", "Reputation Log", "Transactions in Mempool",
            ("Modify Stake" if st.session_state.validator else "Become a Validator"), "Current Block Status", "Broadcasted Blocks", "Enter Page"
        )
}

screen_mapping = {
        "Main Page": "main_page",
        "Upload News": "upload_file",
        "Verified News": "show_blocks",
        "Account Info": "account_info",
        "Sent News": "view_sent_news",
        "Reputation Log": "view_log_reputation",
        "Transactions in Mempool": "show_transac",
        "Modify Stake": "become_validator" if st.session_state.validator else None,
        "Become a Validator": "become_validator" if not st.session_state.validator else None,
        "Current Block Status": "view_block_status",
        "Broadcasted Blocks": "view_sent_blocks",
        "Enter Page": "enter"
    }

def add_space():
    #ADD SPACE
    for i in range(30):
        st.empty()
        
def change_screen_navbar(nav_selection):    
        # Map the nav_selection to corresponding actions
    screen = screen_mapping.get(nav_selection)

    if screen:
        if nav_selection == "Modify Stake" or nav_selection == "Become a Validator":
            st.session_state.stake_submitted = False
            
        if nav_selection == "Upload News":
            st.session_state.upload_file_executed = False

        with st.spinner("Please Wait"):
            change_screen(screen)
            
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
    print("CHANGE SCREEN CALLED ", input_string)
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
